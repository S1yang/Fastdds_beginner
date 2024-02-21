#machine.py
import json
import fastdds
from DataSet import DataSet,DataSetPubSubType # 定义的数据类型


class DDSMachine:
    def __init__(self, mode='both', domain_id=0, topic_name="DataSetTopic"):
        self.mode = mode
        if mode in ['publish', 'both']:
            self.publisher = DDSPublisher(domain_id, topic_name)
        if mode in ['subscribe', 'both']:
            self.subscriber = DDSSubscriber(domain_id, topic_name)

    def process_and_publish_data(self, json_data):
        data_set = self.convert_to_DataSet(json_data)
        self.publish(data_set)

    def convert_to_DataSet(self, json_data):
        data_set = DataSet()
        data_set.message(json_data) 
        return data_set
    
    def publish(self, data_set):

        if hasattr(self, 'publisher'):
            self.publisher.publish(data_set)
        else:
            raise RuntimeError("Publisher not initialized")

    def subscribe(self):
        if hasattr(self, 'subscriber'):
            # 订阅逻辑
            pass
        else:
            raise RuntimeError("Subscriber not initialized")

class DDSPublisher:
    def __init__(self, domain_id=0, topic_name="DataSetTopic"):
        factory = fastdds.DomainParticipantFactory.get_instance()
        self.participant_qos = fastdds.DomainParticipantQos()
        factory.get_default_participant_qos(self.participant_qos)
        self.participant = factory.create_participant(domain_id, self.participant_qos)

        self.topic_data_type = DataSetPubSubType()
        self.type_support = fastdds.TypeSupport(self.topic_data_type)
        self.participant.register_type(self.type_support, self.topic_data_type.getName())

        self.topic_qos = fastdds.TopicQos()
        self.participant.get_default_topic_qos(self.topic_qos)
        self.topic = self.participant.create_topic(topic_name, self.topic_data_type.getName(), self.topic_qos)

        self.publisher_qos = fastdds.PublisherQos()
        self.participant.get_default_publisher_qos(self.publisher_qos)
        self.publisher = self.participant.create_publisher(self.publisher_qos)

        self.writer_qos = fastdds.DataWriterQos()
        self.publisher.get_default_datawriter_qos(self.writer_qos)
        self.writer = self.publisher.create_datawriter(self.topic, self.writer_qos)

    def publish(self, data_set):
        self.writer.write(data_set)

    def __del__(self):
        if self.participant:
            self.participant.delete_contained_entities()
            fastdds.DomainParticipantFactory.get_instance().delete_participant(self.participant)

class DDSSubscriber:
    def __init__(self, domain_id=0, topic_name="DataSetTopic"):
        factory = fastdds.DomainParticipantFactory.get_instance()
        self.participant_qos = fastdds.DomainParticipantQos()
        factory.get_default_participant_qos(self.participant_qos)
        self.participant = factory.create_participant(domain_id, self.participant_qos)

        self.topic_data_type = DataSetPubSubType()
        self.type_support = fastdds.TypeSupport(self.topic_data_type)
        self.participant.register_type(self.type_support, self.topic_data_type.getName())

        self.topic_qos = fastdds.TopicQos()
        self.participant.get_default_topic_qos(self.topic_qos)
        self.topic = self.participant.create_topic(topic_name, self.topic_data_type.getName(), self.topic_qos)

        self.subscriber_qos = fastdds.SubscriberQos()
        self.participant.get_default_subscriber_qos(self.subscriber_qos)
        self.subscriber = self.participant.create_subscriber(self.subscriber_qos)

        self.listener = DDSListener()
        self.reader_qos = fastdds.DataReaderQos()
        self.subscriber.get_default_datareader_qos(self.reader_qos)
        self.reader = self.subscriber.create_datareader(self.topic, self.reader_qos, self.listener)

    def __del__(self):
        if self.participant:
            self.participant.delete_contained_entities()
            fastdds.DomainParticipantFactory.get_instance().delete_participant(self.participant)


class DDSListener(fastdds.DataReaderListener, fastdds.DataWriterListener):
   
    def on_data_available(self, reader):
        info = fastdds.SampleInfo()
        data = DataSet()
        if reader.take_next_sample(data, info) == fastdds.ReturnCode_t.RETCODE_OK:
            if info.instance_state == fastdds.ALIVE_INSTANCE_STATE:
                # 假设我们可以直接访问data.message来获取JSON字符串
                json_data = data.message()
                # 反序列化JSON字符串以获取原始数据
                original_data = json.loads(json_data)
                print("Received data:", original_data)



    def on_subscription_matched(self, reader, info):
        if info.current_count_change > 0:
            print("Subscriber matched with a publisher.")
        else:
            print("Subscriber unmatched from a publisher.")

    def on_publication_matched(self, writer, info):
        # 当发布者匹配或不匹配时触发
        pass



#
# class DDSMachine:
#     def __init__(self,mode='both'):
#
#         self.mode = mode
#
#         ##########以下为DDS相关##########
#         # 创建DomainParticipant
#         factory = fastdds.DomainParticipantFactory.get_instance()
#         self.participant_qos = fastdds.DomainParticipantQos()
#         factory.get_default_participant_qos(self.participant_qos)
#         self.participant = factory.create_participant(0, self.participant_qos)
#
#         # 注册DataSet类型
#         self.topic_data_type = DataSetPubSubType()
#         self.topic_data_type.setName("DataSetDataType")  # 设置类型名称
#         self.type_support = fastdds.TypeSupport(self.topic_data_type)
#         self.participant.register_type(self.type_support, "DataSetDataType")  # 使用设置的类型名称
#
#         # 创建Topic
#         self.topic_qos = fastdds.TopicQos()
#         self.participant.get_default_topic_qos(self.topic_qos)
#         self.topic = self.participant.create_topic("DataSetTopic", "DataSetDataType", self.topic_qos)
#
#         # 根据模式初始化 Publisher 和/或 Subscriber
#         if mode in ['publish', 'both']:
#             self.init_publisher()
#
#         if mode in ['subscribe', 'both']:
#             self.init_subscriber()
#
#     def init_publisher(self):
#         # 创建Publisher和DataWriter
#         self.publisher_qos = fastdds.PublisherQos()
#         self.participant.get_default_publisher_qos(self.publisher_qos)
#         self.publisher = self.participant.create_publisher(self.publisher_qos)
#
#         self.writer_qos = fastdds.DataWriterQos()
#         self.publisher.get_default_datawriter_qos(self.writer_qos)
#         self.writer = self.publisher.create_datawriter(self.topic, self.writer_qos)
#
#     def init_subscriber(self):
#     # 创建Subscriber和DataReader
#         self.subscriber_qos = fastdds.SubscriberQos()
#         self.participant.get_default_subscriber_qos(self.subscriber_qos)
#         self.subscriber = self.participant.create_subscriber(self.subscriber_qos)
#
#         self.reader_qos = fastdds.DataReaderQos()
#         self.subscriber.get_default_datareader_qos(self.reader_qos)
#         self.listener = MyListener()
#         self.reader = self.subscriber.create_datareader(self.topic, self.reader_qos, self.listener)
#
#
#
#
#     def process_and_publish_data(self, data_dict):
#         if data_dict is not None:
#             # self.print_data(data_dict)#test for pub
#             # 将字典数据转换为DDS可识别的DataSet类型
#             data_set = self.convert_to_DataSet(data_dict)
#             # self.print_data(data_set)#test for pub
#             # 发布数据
#             self.publish_data(data_set)
#
#     def convert_to_DataSet(self, data_dict):
#         """
#         将字典形式的数据转换为DataSet对象。
#         """
#         data = DataSet()
#         data.capacity = data_dict.get('capacity', data.capacity)
#         data.remaining_capacity = data_dict.get('remaining_capacity', data.remaining_capacity)
#         data.voltage = data_dict.get('voltage', data.voltage)
#         data.latitude = data_dict.get('latitude', data.latitude)
#         data.longitude = data_dict.get('longitude', data.longitude)
#         data.altitude = data_dict.get('altitude', data.altitude)
#         data.speed = data_dict.get('speed', data.speed)
#         data.direction = data_dict.get('direction', data.direction)
#
#         return data
#
#     def publish_data(self, data_set):
#         # 发布转换后的 DataSet 对象
#         self.print_data_pub(data_set)#test for pub
#         self.writer.write(data_set)
#
#     def print_data_pub(self, data):
#         # *just for test
#         print("Pub data:", data)
#
#     def print_data_sub(self, data):
#         # *just for test
#         print("Received data:", data)
#
# def __del__(self):
#     try:
#         if self.participant:
#             self.participant.delete_contained_entities()
#             fastdds.DomainParticipantFactory.get_instance().delete_participant(self.participant)
#     except Exception as e:
#         print(f"Exception occurred while deleting DDSMachine: {e}")
#
#
# class MyListener(fastdds.DataReaderListener):
#     def on_data_available(self, datareader):
#         # 作用：用于处理接收到的新数据。通常，这里包括从 DataReader 读取数据的逻辑，以及对这些数据进行处理的代码。
#         # 例如，当新的测量数据到达时，可能需要读取这些数据并对其进行处理，如更新UI、存储到数据库或触发其他业务逻辑。
#         # 创建SampleInfo和DataSet实例
#         info = fastdds.SampleInfo()
#         data = DataSet()  # 假设DataSet是我们定义的数据类型
#
#         # 尝试取出下一个样本
#         if datareader.take_next_sample(data, info) == fastdds.ReturnCode_t.RETCODE_OK:
#             if info.instance_state == fastdds.ALIVE_INSTANCE_STATE:
#                 # 处理接收到的数据
#                 print("Received data:", data)
#                 data_dict = self.convert_from_DataSet(data)
#                 # #打印数据
#                 # print("Received data:", data_dict)
#
#
#
#     @staticmethod
#     def convert_from_DataSet(data_set):
#         """
#         将DataSet对象转换为字典形式的数据。
#         """
#         return {
#             'capacity': data_set.capacity(),
#             'remaining_capacity': data_set.remaining_capacity(),
#             'voltage': data_set.voltage(),
#             'latitude': data_set.latitude(),
#             'longitude': data_set.longitude(),
#             'altitude': data_set.altitude(),
#             'speed': data_set.speed(),
#             'direction': data_set.direction()
#         }
#
#     def on_subscription_matched(self, datareader, info):
#         # 这个方法在 DataReader 的订阅状态发生变化时被调用，例如当它与一个 DataWriter 匹配或不匹配时。
#         # 作用：用于处理订阅者状态的更改。这可以包括记录日志、调整UI状态或执行其他与订阅状态相关的操作。
#         # 在建立或失去与数据源的连接时，可能需要执行一些特殊的逻辑，如通知用户或重新配置系统参数。
#         if info.current_count_change > 0:
#             print("Subscriber matched with a publisher.")
#         else:
#             print("Subscriber unmatched from a publisher.")


# import json
# import socket
# import threading
# from enums import Mode
# from enums import DataType
# import zmq
#
# import config
# import function
# from DataStorage import DataStore
# from DataHandler import DataHandler
#
#
# class MQMachine:
#     def __init__(self, name, mode=Mode.TESTMODE, ip=None, port=None, ):
#         """ 初始化MQMachine实例。 """
#         self.name = name
#         self.mode = mode
#         self.container = DataStore()
#         self.running = True
#         self.subscribed_nodes = []  # 添加属性来存储订阅的节点
#
#
#         # 根据 mode 参数选择工作模式
#         if self.mode == Mode.TESTMODE:
#             self.initialize_testmode(ip, port)
#         elif self.mode == Mode.USERMODE:
#             self.initialize_usermode()
#         else:
#             raise ValueError("Invalid mode. Supported modes are 'testmode' and 'usermode'.")
#
#         # 组合 IP 和 port 成为一个 address 字符串
#         self.address = f"{self.ip}:{self.port}"
#         # print(self.address)
#         self.data_handler = DataHandler(self)
#         # 创建 PUB 和 SUB 的上下文
#         self.pub_context = zmq.Context()
#         self.sub_context = zmq.Context()
#
#         # 构建节点并开始监听
#         self.build_node()
#         self.start_listening()
#
#         # self.data_ready_event = threading.Event()
#
#         # 启动UDP接收线程
#         self.udp_thread = threading.Thread(target=self.forward_local_udp)
#         self.udp_thread.start()
#
#
#
#     def initialize_testmode(self, ip, port):
#         # 在 testmode 下，IP 和端口需要明确提供
#         if ip is None or port is None:
#             raise ValueError("For testmode, IP and port must be provided.")
#         self.ip = ip
#         self.port = port
#
#     def initialize_usermode(self):
#         # 在 usermode 下，使用本机 IP 和默认端口
#         self.ip = function.get_local_ip()
#         self.port = "5555"
#         # 注意：这里将端口号设为字符串，确保与 ZMQ 的使用一致
#         # 如果端口号需要为整数，请相应地进行转换
#
#     def build_pub(self, ip_address, port):
#         """ 创建并配置发布者套接字。 """
#         publisher = self.pub_context.socket(zmq.PUB)
#         publisher.bind(f"tcp://{ip_address}:{port}")
#         publisher.setsockopt(zmq.RECONNECT_IVL, 1000)
#         return publisher
#
#
#     def build_sub(self, ips_and_ports):
#         """ 创建并配置订阅者套接字，并订阅特定主题 """
#         subscriber = self.sub_context.socket(zmq.SUB)
#         for ip, port in ips_and_ports:
#             if ip == self.ip and port == self.port:
#                 continue
#             subscriber.connect(f"tcp://{ip}:{port}")
#             self.subscribed_nodes.append((ip, port))  # 将节点添加到订阅列表
#
#         return subscriber
#
#     def get_subscribed_nodes(self):
#         return self.subscribed_nodes
#
#     def build_node(self):
#         """ 创建并保存发布者和订阅者套接字。 """
#         self.publisher = self.build_pub(self.ip, self.port)
#         self.subscriber = self.build_sub(config.IPS_AND_PORTS)
#
#     def publish(self, data):
#         """ 使用发布者套接字发送消息，并包含一个特定主题 """
#         self.publisher.send_string(data)
#         # print(f"DEBUG: Published data on topic '{data}'.")
#
#     def subscribe(self):
#         """ 持续接收订阅者套接字的消息并处理。 """
#         self.subscriber.setsockopt_string(zmq.SUBSCRIBE, "")  # 订阅所有消息
#         while self.running:
#             message = self.subscriber.recv_string()
#             self.data_handler.store_message(message)
#
#     def start_listening(self):
#         """ 在新线程中启动消息订阅监听。 """
#         listener_thread = threading.Thread(target=self.subscribe)
#         listener_thread.start()
#
#
#     def forward_local_udp(self):
#         """接收来自UDP端口5555的数据。转发本地数据到其他节点。"""
#         udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         bind_port = 5555 if self.mode == "usermode" else self.port
#         udp_socket.bind(("127.0.0.1", bind_port))
#
#         while self.running:
#             data, addr = udp_socket.recvfrom(1024)
#             try:
#                 local_udp = json.loads(data.decode())
#                 # print(f"generated udp {local_udp}")
#                 # 使用DataHandler处理数据并存储到容器中
#                 processed_data = self.data_handler.store(local_udp)
#                 # 发布处理后的数据
#                 self.publish(json.dumps(processed_data))
#             except json.JSONDecodeError:
#                 print("Invalid JSON received from UDP.")
#
#     def show_data(self, type, active=False):
#         self.container.print_data(type, active)
#
#     def get_active_data(self, timeout_time):
#         return self.container.get_active_nodes_within(timeout_time)
#
#     def stop(self):
#         """优雅地终止程序并释放资源。"""
#         print("Stopping the MQMachine...")
#
#         # 停止所有循环
#         self.running = False
#
#         # 关闭 ZMQ 套接字
#         if hasattr(self, 'publisher'):
#             self.publisher.close()
#         if hasattr(self, 'subscriber'):
#             self.subscriber.close()
#
#         # 终止 ZMQ 上下文
#         self.pub_context.term()
#         self.sub_context.term()
#
#         # 关闭 UDP 套接字
#         if hasattr(self, 'udp_socket'):
#             self.udp_socket.close()
#
#         # 等待所有线程结束
#         if hasattr(self, 'udp_thread'):
#             self.udp_thread.join()
#         # ... 等待其他线程 ...
#
#         print("MQMachine stopped successfully.")
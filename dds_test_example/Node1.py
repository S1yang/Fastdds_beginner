#Node1.py
from machine import DDSMachine
from SensorDataGenerator import SensorDataGenerator


def main():
    # Initialize the data generator with desired update interval
    generator = SensorDataGenerator(update_interval=10)

    # Initialize DDSMachine in publish mode
    dds_machine = DDSMachine(mode='publish')

    # Set the callback function to publish data
    generator.set_callback(dds_machine.process_and_publish_data)

    # The generate_data_periodically method is assumed to start its own thread
    # and does not block the main thread.

    try:
        # Wait for user input to stop the application
        input("Press Enter to stop...\n")
    except KeyboardInterrupt:
        print("Stopping publisher...")
    finally:
        # Stop the generator's thread
        generator.stop()
        # Additional cleanup if necessary


if __name__ == "__main__":
    main()



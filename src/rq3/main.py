import data_processing
import sentiment_analysis
import result_plotting


def main():
    while True:
        print("\n\n1. Data Processing")
        print("2. Sentiment Analysis")
        print("3. Plot results")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            data_processing.main()
        elif choice == "2":
            sentiment_analysis.main()
        elif choice == "3":
            result_plotting.main()
        else:
            break


main()

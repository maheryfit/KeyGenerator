import getopt, sys

from service import write_in_pem_file

if __name__ == '__main__':
    argumentList = sys.argv[1:]

    # Options
    options = "u:"

    # Long options
    long_options = ["User"]
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-u", "--User"):
                user = currentValue
                write_in_pem_file(user)

    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))
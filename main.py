import getopt, sys

from service import write_in_pem_file, process_sign_file

if __name__ == '__main__':
    argumentList = sys.argv[1:]

    # Options
    options = "u:g:s:"

    # Long options
    long_options = ["User", "Generate", "Sign"]
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        user = ""
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-u", "--User"):
                user = currentValue
            elif currentArgument in ("-g", "--Generate"):
                write_in_pem_file(user)
            elif currentArgument in ("-s", "--Sign"):
                file_path = currentValue
                process_sign_file(file_path, user)

    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))

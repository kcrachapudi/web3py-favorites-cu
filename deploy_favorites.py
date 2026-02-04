from vyper import compile_code

def main():
    print("Let's read in the Vyper code and deploy it!")
    compilation_details = compile_code(favorites_code, output_formats["bytecode"])
    print("Compilation details:", compilation_details)
    
if __name__ == "__main__":
    main()

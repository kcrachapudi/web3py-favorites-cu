from vyper import compile_code

def main():
    print("Let's read in the Vyper code and deploy it!")
    with open("Favorites.vy", "r") as fav_file:
        favorites_code = fav_file.read()
    compilation_details = compile_code(favorites_code, output_formats["bytecode"])
    print("Compilation details:", compilation_details)
    
if __name__ == "__main__":
    main()

import os
import re
import sys

def main():
    # Check for correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python wordCount.py input.txt output.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Dictionary to store word counts
    word_counts = {}
    
    try:
        # Open input file using system calls
        input_fd = os.open(input_file, os.O_RDONLY)
        
        # Read the entire file content
        content = b""
        while True:
            chunk = os.read(input_fd, 4096)
            if not chunk:
                break
            content += chunk
        
        # Close input file
        os.close(input_fd)
        
        # Convert bytes to string and convert to lowercase
        text = content.decode('utf-8').lower()
        
        # Replace hyphens with spaces to split compound words
        text = text.replace('-', ' ')
        
        # More careful apostrophe handling - only remove apostrophe if it's possessive
        text = re.sub(r"(\w)'s\b", r"\1 ", text)  # Replace "word's" with "word "
        text = text.replace("'", " ")  # Replace other apostrophes with space
        
        # Use regex to find words - include single letters
        words = re.findall(r'\b[a-z]\b|\b[a-z][a-z]*\b', text)
        
        # Count word occurrences
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        # Sort words alphabetically to match key files
        sorted_words = sorted(word_counts.items(), key=lambda x: x[0])
        
        # Open output file using system calls
        output_fd = os.open(output_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
        
        # Write results to output file
        for word, count in sorted_words:
            line = f"{word} {count}\n"
            os.write(output_fd, line.encode('utf-8'))
        
        # Close output file
        os.close(output_fd)
        
        print(f"Word count completed. Results written to {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
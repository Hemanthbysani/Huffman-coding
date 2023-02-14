import heapq
import collections
# ENCODING
def huffman_encoding():
    # Read the input file and count the frequency of each character
    with open("input.txt", "r") as file_input:
        freq = collections.Counter(file_input.read())
        file_input.close()

    # Build the Huffman tree
    heap = [[weight, [symbol, ""]] for symbol, weight in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    # Generate the encoding for each character
    global encoding 
    encoding = {}
    for pair in heapq.heappop(heap)[1:]:
        encoding[pair[0]] = pair[1]
    global before_compression
    with open("input.txt", "r") as file_input:
        data = file_input.read()
        before_compression = len(data) * 8
        file_input.close()

    # Write the encoded output to the output file
    # print(encoding)
    with open("encoding.txt", "w") as file_outt:
        file_outt.write(str(encoding))
        file_outt.close()
    with open("encoded.txt", "w") as file_output:
        with open("input.txt", "r") as file_input:
            # print(file_input.read())
            file_output.write("".join([encoding[ch] for ch in file_input.read()]))
            file_input.close()
        file_output.close()

    

huffman_encoding()
# First, we create a list of nodes, where each node is a list containing the frequency of the character and a list of the character and its code. For example, the node for the character "a" with frequency 3 would be [3, ["a", ""]].
# We then create a heap from this list of nodes using the heapify function from the heapq module. This function rearranges the list in-place to form a heap.
# We enter a loop that continues until the heap has only one node left (the root of the tree). Within the loop, we pop the two nodes with the lowest frequencies off the heap using the heappop function. These nodes will become the children of a new parent node.
# For each character in the left child (the node with the lower frequency), we prepend a "0" to its code. For each character in the right child (the node with the higher frequency), we prepend a "1" to its code.
# We then create a new parent node with the sum of the frequencies of the two children as its frequency, and the two children as its children.
# Finally, we push the new parent node back onto the heap using the heappush function.
# This process continues until the heap has only one node left, at which point the tree is complete. The codes for each character can then be extracted from the tree by traversing the tree and looking at the code for each character.

# GAIN CALCULATION
after_compression = 0
symbols = encoding.keys()
for symbol in symbols:
    with open("input.txt", "r") as file_input:
         data = file_input.read()
    count = data.count(symbol)
    after_compression += count * len(encoding[symbol])
file_input.close()
print("Space usage before compression (in bits):", before_compression)    
print("Space usage after compression (in bits):",  after_compression)

# DECODING
def huffman_decoding():
    # Read the Huffman encoding from a file
    encoding = {}
    try:
        with open("encoding.txt", "r") as file_input:
            for line in file_input:
                for elements in line.split(","):
                    # print(elements)
                    ch, code = elements.replace("'","").replace("{", "").replace("}","").strip().split(": ")
                    encoding[ch] = code
            # print(encoding)
    except FileNotFoundError:
        print("Error: The file 'encoding.txt' does not exist.")
        return

    # Read the encoded data from a file
    try:
        with open("encoded.txt", "r") as file_input:
            encoded = file_input.read()
            file_input.close()
    except FileNotFoundError:
        print("Error: The file 'encoded.txt' does not exist.")
        return

    # Decode the encoded data
    decoded = ""
    current_code = ""
    if encoded:
        for ch in encoded:
            current_code += ch
            if current_code in encoding.values():
                # print(current_code)
                value = {i for i in encoding if encoding[i]==current_code}
                decoded += (list(value)[0])
                current_code = ""

    # Write the decoded data to a file
    with open("decoded.txt", "w") as file_output:
        file_output.write(decoded)
        file_output.close()


huffman_decoding()
# The function huffman_decoding takes two file objects as arguments: file_in and file_out. The file_in object is used to read the Huffman encoding and the encoded message from the input file, and the file_out object is used to write the decoded message to the output file.
# The first step in the decoding process is to read the Huffman encoding from the input file. This is done by looping through each line in the file and splitting it on the colon character (":"). The left side of the colon is the character, and the right side is the code. These values are then added to the encoding dictionary, with the code as the key and the character as the value.
# The next step is to decode the encoded message. To do this, we initialize an empty string called decoded and a string called current_code that will be used to store the code that we are currently building up as we read the encoded message.
# We then loop through each character in the encoded message, adding it to the current_code string. If the current_code string is in the encoding dictionary, we append the corresponding character to the decoded string and reset the current_code string to be empty. If the current_code string is not in the encoding dictionary, we continue adding characters to it until we find a matching code.
# Finally, we write the decoded string to the output file using the file_out object. This completes the decoding process.
# To decode the encoded message, the decoder reads the encoding file and builds a dictionary that maps the codes to the corresponding characters. It then reads the encoded message one character at a time, adding the characters to a current code until it finds a matching code in the dictionary. When a matching code is found, the decoder adds the corresponding character to the decoded message and resets the current code to be empty. This process is repeated until the entire encoded message has been decoded.

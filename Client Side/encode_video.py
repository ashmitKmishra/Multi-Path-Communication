import os
import random

def encode_file(input_file, output_directory):

    with open(input_file, 'rb') as file:
        input_image = file.read()

       #converts string into binary
        M = ''.join(format(byte, '08b') for byte in input_image) 
        #this will make everything even

    length_M = len(M)
    print(length_M)

    if length_M % 2 != 0:
        M.append(0)  # Append '0' as a string if the length of M is not even 
        E1_header = [1,0,1]
        E2_header = [1,1,0]
        E3_header = [1,1,1]
    else: 
        E1_header = [0,0,1]
        E2_header = [0,1,0]
        E3_header = [0,1,1]

    half_len = len(M) // 2 

    # Now we split M into two equal parts M1 and M2
    M1 = M[:half_len]
    M2 = M[half_len:]
    
    
    # R1 and R2 are two independent sequences of bits uniformly distributed over {0, 1}^(M/2)
    R1 = [random.randint(0, 1) for _ in range(half_len)]
    R2 = [random.randint(0, 1) for _ in range(half_len)]
    #print(M) #checker

    # 3 encoded parts
    # E1
    #E1_header #value depends upon the if length of M is even or odd
    E1_raw = [R1[i] for i in range(half_len)] + [int(M2[i]) ^ R2[i] for i in range(half_len)]
    E1 = E1_header + E1_raw #added indicator 1 in binary to represent it is E1 chunk

    # E2
    #E2_header #value depends upon the if length of M is even or odd
    E2_raw= [int(M1[i]) ^ R1[i] for i in range(half_len)] + [R2[i] for i in range(half_len)]
    E2= E2_header+E2_raw #added indicator 2 in binary to represent it is E2 chunk 
 
    # E3
    #E3_header #value depends upon the if length of M is even or odd
    E3_raw = [int(M1[i]) ^ R2[i] for i in range(half_len)] + [int(M2[i]) ^ R1[i] for i in range(half_len)]
    E3= E3_header+E3_raw #added indicator 3 in binary to represent it is E3 chunk

    #print("E1")
    #print(E1)

    #print("E1_raw")
    #print(len(E1))
    #print(len(E1))
    #print(E1_raw)
    #print(E2)
    #print(E3)

    #print(type(E1_header))

    file_paths = []
    for i, encoded_file in enumerate([E1, E2, E3]):
        file_name = f"E{i + 1}.bin"
        file_path = os.path.join(output_directory, file_name)
        with open(file_path, 'wb') as file:
            file.write(bytes(encoded_file))
        file_paths.append(file_path)

    return file_paths

input_file = 'video.mp4'  
output_directory = 'encoded_files'  

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

encoded_file_paths = encode_file(input_file, output_directory)
print("Encoded files saved at:")
for path in encoded_file_paths:
    print(path)

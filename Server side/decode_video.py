import os

def decode_file(files_found):
    E1, E2, E3 = None, None, None

    for file_name in files_found:
        file_path = os.path.join(encoded_files_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                print(f"File Name: {file_name}")
                
                first_1_letter = f.read(1)
                print(f"First 1 Letter: {first_1_letter}")
                first_3_letters = f.read(2)
                print(f"Second 2 Letters: {first_3_letters}")

                if first_1_letter == b'\x01':
                    if first_3_letters == b'\x00\x01':
                        E1 = list(f.read()[-1])
                    elif first_3_letters == b'\x01\x00':
                        E2 = list(f.read()[-1])
                    elif first_3_letters == b'\x01\x01':
                        E3 = list(f.read()[-1])
                elif first_1_letter == b'\x00':
                    if first_3_letters == b'\x00\x01':
                        E1 = list(f.read())
                    elif first_3_letters == b'\x01\x00':
                        E2 = list(f.read())
                    elif first_3_letters == b'\x01\x01':
                        E3 = list(f.read())

    if E1 is not None and E2 is not None:
        half_length = len(E1) // 2
        print("**Through E1 and E2:**")

        R1 = E1[:half_length]
        R2 = E2[half_length:]

        M1 = [E2[i] ^ R1[i] for i in range(half_length)]
        M2 = [E1[half_length + i] ^ R2[i] for i in range(half_length)]

        M = M1 + M2
        return M
    elif E1 is not None and E3 is not None:
        half_length = len(E1) // 2
        print("**Through E1 and E3**")

        R1 = E1[:half_length]
        M2 = [E3[half_length + i] ^ R1[i] for i in range(half_length)]

        R2 = [E1[half_length + i] ^ M2[i] for i in range(half_length)]
        M1 = [E3[i] ^ R2[i] for i in range(half_length)]

        M = M1 + M2
        return M
    elif E2 is not None and E3 is not None:
        half_length = len(E2) // 2
        print("**Through E2 and E3**")

        R2 = E2[half_length:]
        M1 = [E3[i] ^ R2[i] for i in range(half_length)]

        R1 = [E2[i] ^ M1[i] for i in range(half_length)]
        M2 = [E3[half_length + i] ^ R1[i] for i in range(half_length)]

        M = M1 + M2
        return M
    else:
        print("Failed to find valid E1, E2, or E3")
        return []

encoded_files_path = os.path.join(os.getcwd(), 'encoded_files')
files_found = os.listdir(encoded_files_path)

# Call the decode_file function
binary_data = decode_file(files_found)
# Assuming binary_data is a list of integers representing binary digits, e.g., [1, 0, 1, 1, 0, 1, 0, 0]

if binary_data:
    binary_string = ''.join(str(bit) for bit in binary_data)  # Convert the list to a string: '10110100'
    recovered_image = bytearray([int(binary_string[i:i + 8], 2) for i in range(0, len(binary_string), 8)])
    file_name1 = "recovered_video.mp4"
    with open(file_name1, 'wb') as file:
        file.write(recovered_image)
    print(f'File is saved to {file_name1}')
else:
    print("Decoding failed.")


text = input("Enter some text: ")

print("\n🔹 String Manipulator Results 🔹")
print(f"Original text: {text}")
print(f"Uppercase: {text.upper()}")
print(f"Lowercase: {text.lower()}")
print(f"Title Case: {text.title()}")
print(f"Reversed: {text[::-1]}")
print(f"Word Count: {len(text.split())}")
print(f"Character Count (no spaces): {len(text.replace(' ', ''))}")

word_to_replace = input("\nEnter word to replace: ")
replacement = input("Enter replacement: ")
print(f"Updated text: {text.replace(word_to_replace, replacement)}")

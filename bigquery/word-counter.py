from collections import Counter
import pandas as pd

# Ścieżka do pliku z tekstem
file_path = 't8.shakespeare.txt'

# Funkcja licząca słowa w pliku
def count_words(file_path):
    # Otwórz i odczytaj plik
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    # Zmień tekst na małe litery i podziel na słowa
    words = text.lower().split()
    # Usuń znaki interpunkcyjne z każdego słowa
    words = [word.strip(".,!?\"'():;[]{}") for word in words]
    # Policz wystąpienia każdego słowa
    word_counts = Counter(words)
    return word_counts

# Licz słowa w pliku
word_counts = count_words(file_path)

# Konwersja wyników na DataFrame
df = pd.DataFrame(word_counts.items(), columns=['word', 'sum_word_count'])
df = df.sort_values(by='sum_word_count', ascending=False)

# Wyświetlenie wyników
print(df)

# Opcjonalnie: zapis wyników do pliku CSV
output_file = 'word_count.csv'
df.to_csv(output_file, index=False)
print(f"Word count saved to {output_file}")
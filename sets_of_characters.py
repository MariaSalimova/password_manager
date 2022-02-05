# наборы символов для паролей
letters = set('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')
numbers = set('1234567890')
symbols = set('!@#$%^&*()_+-=?№;:/.,~[]{}')
letters_numbers = letters.union(numbers)
letters_numbers_symbols = letters_numbers.union(symbols)

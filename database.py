import pandas as pd
import numpy as np
import os
from datetime import datetime


def create_test_data():
    """Создает тестовые данные если файл не найден"""
    print("Создаем тестовые данные...")
    np.random.seed(42)
    n_rows = 50

    data = {
        'Booking ID': range(1, n_rows + 1),
        'booking_datetime': [datetime(2024, 3, np.random.randint(1, 32),
                                      np.random.randint(0, 24),
                                      np.random.randint(0, 60)) for _ in range(n_rows)],
        'Booking Status': np.random.choice(['Completed', 'Cancelled by Driver', 'Cancelled by User', 'In Progress'],
                                           n_rows),
        'Vehicle Type': np.random.choice(['Auto', 'Sedan', 'SUV', 'Bike'], n_rows),
        'Payment Method': np.random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Cash'], n_rows),
        'Booking Value': np.random.uniform(100, 1000, n_rows).round(2)
    }

    return pd.DataFrame(data)


def main():
    # Шаг 1: Загрузка данных
    print("=" * 60)
    print("ШАГ 1: ЗАГРУЗКА И ПЕРВИЧНЫЙ ОСМОТР ДАННЫХ")
    print("=" * 60)

    # Попытка загрузки файла
    file_found = False
    possible_filenames = [
        'datecer_uber_pides_bookings.csv',
        'data_uber_rides_bookings.csv',
        'uber_data.csv',
        'bookings.csv',
        'data.csv'
    ]

    for filename in possible_filenames:
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            print(f"✓ Файл '{filename}' успешно загружен!")
            file_found = True
            break

    if not file_found:
        print("✗ CSV файл не найден. Создаем тестовые данные...")
        df = create_test_data()
        print("✓ Тестовые данные созданы успешно!")

    print("\n" + "=" * 40)

    # 2. Вывод первых 5 строк
    print("1. Первые 5 строк данных:")
    print(df.head())
    print("\n" + "-" * 40)

    # 3. Общая информация о датасете
    print("2. Общая информация о датасете:")
    df.info()
    print("\n" + "-" * 40)

    # 4. Статистическое описание числовых столбцов
    print("3. Статистическое описание числовых столбцов:")
    print(df.describe())
    print("\n" + "-" * 40)

    # 5. Количество строк и столбцов
    print("4. Количество строк и столбцов:")
    print(f"Строк: {df.shape[0]}, Столбцов: {df.shape[1]}")

    print("\n" + "=" * 60)
    print("ШАГ 3: ВЫБОРКА И ФИЛЬТРАЦИЯ ДАННЫХ")
    print("=" * 60)

    # 1. Выборка определенных столбцов
    print("1. Выборка столбцов Booking ID, booking_datetime, Booking Status, Vehicle Type, Payment Method:")
    selected_columns = ['Booking ID', 'booking_datetime', 'Booking Status', 'Vehicle Type', 'Payment Method']

    # Проверяем, какие столбцы действительно существуют в DataFrame
    available_columns = [col for col in selected_columns if col in df.columns]
    if available_columns:
        subset_df = df[available_columns]
        print("Первые 5 строк:")
        print(subset_df.head())
    else:
        print("Ни один из запрошенных столбцов не найден в данных")
        print("Доступные столбцы:", list(df.columns))
    print("\n" + "-" * 40)

    # 2. Фильтрация отмененных водителем бронирований
    print("2. Бронирования, отмененные водителем:")
    if 'Booking Status' in df.columns:
        cancelled_by_driver = df[df['Booking Status'] == 'Cancelled by Driver']
        print(f"Найдено: {len(cancelled_by_driver)} записей")
        if len(cancelled_by_driver) > 0:
            print(cancelled_by_driver)
        else:
            print("Записи с статусом 'Cancelled by Driver' не найдены")
            print("Доступные статусы:", df['Booking Status'].unique())
    else:
        print("Столбец 'Booking Status' не найден")
    print("\n" + "-" * 40)

    # 3. Фильтрация Auto с Booking Value > 500
    print("3. Бронирования Auto с Booking Value > 500:")
    conditions_met = True

    if 'Vehicle Type' not in df.columns:
        print("Столбец 'Vehicle Type' не найден")
        conditions_met = False

    if 'Booking Value' not in df.columns:
        print("Столбец 'Booking Value' не найден")
        conditions_met = False

    if conditions_met:
        auto_high_value = df[(df['Vehicle Type'] == 'Auto') & (df['Booking Value'] > 500)]
        print(f"Найдено: {len(auto_high_value)} записей")
        if len(auto_high_value) > 0:
            print(auto_high_value)
        else:
            print("Записи не найдены")
            print("Доступные Vehicle Type:", df['Vehicle Type'].unique())
    print("\n" + "-" * 40)

    # 4. Фильтрация бронирований за март 2024
    print("4. Бронирования за март 2024 года:")
    if 'booking_datetime' in df.columns:
        try:
            # Преобразуем в datetime
            df['booking_datetime'] = pd.to_datetime(df['booking_datetime'])

            # Фильтрация по дате
            march_2024_bookings = df[
                (df['booking_datetime'] >= '2024-03-01') &
                (df['booking_datetime'] <= '2024-03-31')
                ]
            print(f"Найдено: {len(march_2024_bookings)} записей")
            if len(march_2024_bookings) > 0:
                print(march_2024_bookings)
            else:
                print("Бронирования за март 2024 не найдены")
                print("Диапазон дат в данных:")
                print(f"От: {df['booking_datetime'].min()}")
                print(f"До: {df['booking_datetime'].max()}")

        except Exception as e:
            print(f"Ошибка при обработке дат: {e}")
    else:
        print("Столбец 'booking_datetime' не найден")

    print("\n" + "=" * 60)
    print("ВСЕ ЗАДАНИЯ ВЫПОЛНЕНЫ!")
    print("=" * 60)


if __name__ == "__main__":
    main()
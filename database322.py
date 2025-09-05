import pandas as pd
import numpy as np
import os
from datetime import datetime


def main():
    # Шаг 1: Загрузка данных
    print("=" * 60)
    print("ШАГ 1: ЗАГРУЗКА И ПЕРВИЧНЫЙ ОСМОТР ДАННЫХ")
    print("=" * 60)

    # Загрузка файла с правильным именем
    filename = 'uber_rides_bookings.csv'
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        print(f"✓ Файл '{filename}' успешно загружен!")
        print(f"Загружено {len(df)} записей")
    else:
        print(f"✗ Файл '{filename}' не найден!")
        print("Проверьте наличие файла в директории")
        return

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

    # 1. Выборка определенных столбцов (правильные столбцы)
    print("1. Выборка столбцов Booking ID, booking_datetime, Booking Status, Vehicle Type, Payment Method:")

    # Проверяем наличие столбца booking_datetime
    if 'booking_datetime' in df.columns:
        selected_columns = ['Booking ID', 'booking_datetime', 'Booking Status', 'Vehicle Type', 'Payment Method']
    else:
        # Если booking_datetime нет, используем Date и Time
        print("Столбец 'booking_datetime' не найден, используем Date и Time")
        selected_columns = ['Booking ID', 'Date', 'Time', 'Booking Status', 'Vehicle Type', 'Payment Method']

    # Проверяем, какие столбцы действительно существуют
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
            print(cancelled_by_driver.head())
        else:
            print("Записи с статусом 'Cancelled by Driver' не найдены")
            print("Доступные статусы:", df['Booking Status'].unique())
    else:
        print("Столбец 'Booking Status' не найден")
    print("\n" + "-" * 40)

    # 3. Фильтрация Auto с Booking Value > 500
    print("3. Бронирования Auto с Booking Value > 500:")

    if 'Vehicle Type' in df.columns and 'Booking Value' in df.columns:
        auto_high_value = df[(df['Vehicle Type'] == 'Auto') & (df['Booking Value'] > 500)]
        print(f"Найдено: {len(auto_high_value)} записей")
        if len(auto_high_value) > 0:
            print(auto_high_value[['Booking ID', 'Vehicle Type', 'Booking Value']].head())
        else:
            print("Записи не найдены")
            print("Уникальные Vehicle Type:", df['Vehicle Type'].unique())
            print("Максимальное Booking Value:", df['Booking Value'].max())
    else:
        missing_cols = []
        if 'Vehicle Type' not in df.columns:
            missing_cols.append('Vehicle Type')
        if 'Booking Value' not in df.columns:
            missing_cols.append('Booking Value')
        print(f"Отсутствуют столбцы: {missing_cols}")
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
                print(march_2024_bookings[['Booking ID', 'booking_datetime', 'Booking Status']].head())
            else:
                print("Бронирования за март 2024 не найдены")
                print("Диапазон дат в данных:")
                print(f"От: {df['booking_datetime'].min()}")
                print(f"До: {df['booking_datetime'].max()}")

        except Exception as e:
            print(f"Ошибка при обработке дат: {e}")
    elif 'Date' in df.columns:
        try:
            # Пытаемся использовать столбец Date
            df['Date'] = pd.to_datetime(df['Date'])
            march_2024_bookings = df[
                (df['Date'] >= '2024-03-01') &
                (df['Date'] <= '2024-03-31')
                ]
            print(f"Найдено: {len(march_2024_bookings)} записей (по столбцу Date)")
            if len(march_2024_bookings) > 0:
                print(march_2024_bookings[['Booking ID', 'Date', 'Booking Status']].head())
        except Exception as e:
            print(f"Ошибка при обработке Date: {e}")
    else:
        print("Столбцы с датами не найдены")

    print("\n" + "=" * 60)
    print("ВСЕ ЗАДАНИЯ ВЫПОЛНЕНЫ!")
    print("=" * 60)


if __name__ == "__main__":
    main()
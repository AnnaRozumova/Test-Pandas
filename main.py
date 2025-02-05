import pandas

class DataFrameHandler():
    def __init__(self, filepath):
        self.df = pandas.read_csv(filepath)

    def update_csv(self):
        return self.df.to_csv('updated.csv', index=False)
    
    def show_info(self):
        return self.df.info()
    
    def get_list_of_properties(self):
        return list(self.df.columns)
    
    def types_of_properties(self):
        return self.df.dtypes
    
    def maximum_numeric_value(self, prop):
        return self.df[prop].max()
    
    def minimum_numeric_value(self, prop):
        return self.df[prop].min()
    
    def get_unique_values(self, prop):
        if prop in self.df.columns:
            return self.df[prop].unique()
        else:
            return []
    
    def filter_by_value(self, prop, value):
        if prop not in self.df.columns:
            print(f"Property '{prop}' not found in the CSV file.")
            return self.df.iloc[0:0]
        
        col_dtype = self.df[prop].dtype
        if pandas.api.types.is_numeric_dtype(col_dtype):
            try:
                numeric_value = float(value)
            except ValueError:
                print(f"Input value '{value}' cannot be converted to a number.")
                return self.df.iloc[0:0]
            filtered = self.df[self.df[prop] == numeric_value]
        else:
            filtered = self.df[self.df[prop].astype(str) == value]
        return filtered
    
    def create_rule(self, rules):
        filtered = self.df
        for prop, value in rules.items():
            if value == "":
                continue

            if prop not in filtered.columns:
                print(f"Property '{prop}' not found in the CSV file. Skipping...")
                continue

            col_dtype = filtered[prop].dtype
            if pandas.api.types.is_numeric_dtype(col_dtype):
                try:
                    numeric_value = float(value)
                except ValueError:
                    print(f"Invalid numeric value '{value}' for property '{prop}'. Skipping this rule.")
                    continue
                filtered = filtered[filtered[prop] == numeric_value]
            else:
                filtered = filtered[filtered[prop].astype(str) == value]
        return filtered


def main():
    filepath = input("Enter the CSV file path: ").strip()
    
    try:
        handler = DataFrameHandler(filepath)
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return

    while True:
        search = str(input("\nDo you want to make simple search(1) or complex search(2)? (Enter 1 or 2): ").strip())
        if search == '1':
            print("\n--- Available Properties ---")
            properties = handler.get_list_of_properties()
            for prop in properties:
                print(f"- {prop}")
            
            selected_prop = input("\nEnter the property (column) you want to inspect: ").strip()
            if selected_prop not in properties:
                print(f"Property '{selected_prop}' not found in the CSV file. Please try again.")
                continue
            
            unique_values = handler.get_unique_values(selected_prop)
            if len(unique_values) == 0:
                print(f"No values found for property '{selected_prop}'.")
                continue

            print(f"\nUnique values for '{selected_prop}':")
            for value in unique_values:
                print(f"- {value}")

            selected_value = input(f"\nEnter a value to filter the rows by for '{selected_prop}': ").strip()
            filtered_df = handler.filter_by_value(selected_prop, selected_value)
            
            print("\n--- Filtered Rows ---")
            if filtered_df.empty:
                print(f"No rows found with {selected_prop} = '{selected_value}'.")
            else:
                print(filtered_df)
                count = len(filtered_df)
                print(f"\nThere are {count} items with {selected_prop} = '{selected_value}'.")

        elif search == '2':
            print("\n--- Complex Search ---")
            print("Enter filter criteria for each property. Leave blank to ignore a property.")
            rules = {}
            for prop in handler.get_list_of_properties():
                value = input(f"Enter value for '{prop}' (or press Enter to skip): ").strip()
                rules[prop] = value

            filtered_df = handler.create_rule(rules)
            
            print("\n--- Filtered Rows ---")
            if filtered_df.empty:
                print("No rows found matching the given criteria.")
            else:
                print(filtered_df)
                count = len(filtered_df)
                print(f"\nFound {count} items matching the given criteria.")


        else:
            print("\nPlease enter 1 or 2 to choose the way of search.")
        
        again = input("\nDo you want to perform another search? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
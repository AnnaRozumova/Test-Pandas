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
    
    def create_rule(self, filters):
        query_parts = []

        for prop, value in filters.items():
            if isinstance(value, tuple): 
                min_val, max_val = value
                if min_val is not None and max_val is not None:
                    query_parts.append(f"({prop} >= {min_val} and {prop} <= {max_val})")
                elif min_val is not None:
                    query_parts.append(f"{prop} >= {min_val}")
                elif max_val is not None:
                    query_parts.append(f"{prop} <= {max_val}")
            else:  
                query_parts.append(f"{prop} == '{value}'")

        query_string = " and ".join(query_parts)

        try:
            return self.df.query(query_string) if query_string else self.df
        except Exception as e:
            print(f"Error in query: {e}")
            return self.df.iloc[0:0] 



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

            filters = {}
            for prop in handler.get_list_of_properties():
                col_dtype = handler.df[prop].dtype

                if pandas.api.types.is_numeric_dtype(col_dtype):
                    min_val = input(f"Enter minimum value for '{prop}' (or press Enter to skip): ").strip()
                    max_val = input(f"Enter maximum value for '{prop}' (or press Enter to skip): ").strip()

                    min_val = float(min_val) if min_val else None
                    max_val = float(max_val) if max_val else None

                    if min_val is not None or max_val is not None:
                        filters[prop] = (min_val, max_val)

                else:
                    value = input(f"Enter value for '{prop}' (or press Enter to skip): ").strip()
                    if value:
                        filters[prop] = value

            filtered_df = handler.create_rule(filters)

            print("\n--- Filtered Rows ---")
            if filtered_df.empty:
                print("No rows found matching the given criteria.")
            else:
                print(filtered_df)
                print(f"\nFound {len(filtered_df)} items matching the given criteria.")


        else:
            print("\nPlease enter 1 or 2 to choose the way of search.")
        
        again = input("\nDo you want to perform another search? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
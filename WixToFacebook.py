import pandas as pd
import sqlite3
import requests
from googlesearch import search
from bs4 import BeautifulSoup

def transform_wix_to_facebook(wix_csv_path, output_csv_path, db_path):
    # Load the Wix CSV file
    wix_df = pd.read_csv(wix_csv_path)

    # Create a new DataFrame for Facebook Commerce Manager
    fb_df = pd.DataFrame()

    # Map Wix columns to Facebook Commerce Manager columns
    fb_df['id'] = wix_df['handleId']
    fb_df['title'] = wix_df['name'].where(wix_df['fieldType'] == 'Product', None)
    fb_df['title'] = fb_df['title'].ffill()
    fb_df['description'] = wix_df['description']
    fb_df['availability'] = wix_df['visible'].apply(lambda x: 'in stock' if x else 'out of stock')  # Assuming 'visible' is True/False
    fb_df['condition'] = 'new'  # Assuming all items are new; adjust as necessary
    fb_df['price'] = wix_df['price'].where(wix_df['fieldType'] == 'Product', None)
    fb_df['price'] = fb_df['price'].ffill()
    fb_df['link'] = wix_df['productImageUrl']  # Adjust if you have a specific product link
    fb_df['image_link'] = wix_df['productImageUrl']  # Adjust if you have a specific image URL
    fb_df['brand'] = wix_df['brand']
    fb_df['google_product_category'] = 'Your_Category'  # Specify your category here
    fb_df['fb_product_category'] = wix_df['collection']
    fb_df['quantity_to_sell_on_facebook'] = wix_df['inventory']
    fb_df['sale_price'] = wix_df['discountValue']  # Adjust as necessary
    fb_df['sale_price_effective_date'] = ''  # Placeholder; set this if you have a date
    fb_df['item_group_id'] = wix_df['handleId']  # Adjust if grouping is necessary
    fb_df['gender'] = ''  # Placeholder; adjust as necessary
    fb_df['color'] = wix_df['productOptionName1']  # Assuming this is the color option
    fb_df['size'] = wix_df['productOptionDescription1']  # Assuming this is the size option
    fb_df['age_group'] = ''  # Placeholder; adjust as necessary
    fb_df['material'] = ''  # Placeholder; adjust as necessary
    fb_df['pattern'] = ''  # Placeholder; adjust as necessary
    fb_df['shipping'] = ''  # Placeholder; adjust as necessary
    fb_df['shipping_weight'] = wix_df['weight']
    fb_df['video[0].url'] = ''  # Placeholder; adjust if you have video URLs
    fb_df['video[0].tag[0]'] = ''  # Placeholder; adjust if you have tags
    fb_df['gtin'] = ''  # Placeholder; adjust if you have GTINs
    fb_df['product_tags[0]'] = ''  # Placeholder; adjust if you have tags
    fb_df['product_tags[1]'] = ''  # Placeholder; adjust if you have tags
    fb_df['style[0]'] = ''  # Placeholder; adjust if you have style

    

    # Save the transformed DataFrame to a new CSV file
    fb_df.to_csv(output_csv_path, index=False)
    print(f"Transformed data saved to {output_csv_path}")

    # Save the DataFrame to an SQLite database
    with sqlite3.connect(db_path) as conn:
        fb_df.to_sql('products', conn, if_exists='replace', index=False)
        print(f"Data saved to SQLite database at {db_path}")


def search_product_url(product_name):
    query = f"{product_name} site:fenclawandfaund.com"
    print(f"Query: {query}")  # Debug: Check the query

    try:
        # Collect results in a list
        results = list(search(query, num_results=1))  # Convert the generator to a list
        if results:
            print(f"Found results: {results}")  # Debug: Print found results
            return results[0]  # Return the first result or None
        else:
            print("No results found.")
            return None
    except Exception as e:
        print(f"Error fetching search results for {product_name}: {e}")
        return None


result = search_product_url('Cult of Mathilda Apprentices handbook')
print(result)

# Example usage
transform_wix_to_facebook(r'C:\Users\Dreid\Desktop\Brain\Projects\Wix to Facebook conversion\output_catalog.csv', r'C:\Users\Dreid\Desktop\Brain\Projects\Wix to Facebook conversion\facebook_output_products.csv', r'C:\Users\Dreid\Desktop\Brain\Projects\Wix to Facebook conversion\facebook_products.db')
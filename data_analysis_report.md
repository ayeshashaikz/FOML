# Logistics Dataset Analysis Report

## Overview
An analysis was performed on the existing e-commerce logistics dataset (`Train.csv`) to prepare the data for Delivery Delay Prediction and Route Optimization.

## Dataset Profile
- **Total Records:** 10,999
- **Total Features:** 12
- **Missing Values:** None (0 missing values across all columns)

## Feature Evaluaton
Here is an evaluation of the original features and their relevance:

1. **ID**: Unique identifier. *(Discarded - No predictive power)*
2. **Warehouse_block**: The warehouse from which the product was dispatched (A, B, C, D, E, F). *(Kept - Essential for route optimization origin points and regional delay prediction)*
3. **Mode_of_Shipment**: The method of transport (Flight, Ship, Road). *(Kept - Critical for both route planning speeds and delivery delay estimation)*
4. **Customer_care_calls**: Number of calls made by the customer. *(Discarded - Typically a post-dispatch or reactive metric, less useful for pre-dispatch delay prediction)*
5. **Customer_rating**: Customer's rating. *(Discarded - Post-delivery metric)*
6. **Cost_of_the_Product**: Cost of the item. *(Kept - May correlate with priority routing or special handling leading to different delay profiles)*
7. **Prior_purchases**: Number of prior purchases. *(Discarded - Customer history does not directly impact physical routing/delays)*
8. **Product_importance**: The importance level of the product (low, medium, high). *(Kept - Important for priority routing and delay prediction)*
9. **Gender**: Customer's gender. *(Discarded - Irrelevant to logistics/routing)*
10. **Discount_offered**: Discount provided. *(Kept - Could be correlated with shipping service tiers or product clearance profiles)*
11. **Weight_in_gms**: Weight of the product. *(Kept - Extremely critical for vehicle capacity constraints in route optimization and correlated with transport speed)*
12. **Reached.on.Time_Y.N**: Target variable (1 = Not on time, 0 = On time). *(Kept - The primary target variable for the delay prediction model)*

## Action Taken
We successfully filtered the dataset to include only the predictive and routing-relevant columns:
`['Warehouse_block', 'Mode_of_Shipment', 'Product_importance', 'Weight_in_gms', 'Cost_of_the_Product', 'Discount_offered', 'Reached.on.Time_Y.N']`

The filtered dataset has been successfully saved to **`delivery_optimization_data.csv`** and is ready for model training and ML processing.

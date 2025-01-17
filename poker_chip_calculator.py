import streamlit as st

# Function to calculate poker chips required for a buy-in
def calculate_chips(amount, chip_values, min_whites, min_reds, max_blacks):
    chip_count = {color: 0 for color in chip_values}
    remaining_amount = int(amount * 10)  # Scale to avoid float issues

    # Scale chip values to integers
    scaled_chip_values = {color: int(value * 10) for color, value in chip_values.items()}

    # Fix White, Red, and Black chips
    chip_count["White"] = min_whites
    chip_count["Red"] = min_reds
    chip_count["Black"] = max_blacks
    remaining_amount -= int(min_whites * scaled_chip_values["White"] + min_reds * scaled_chip_values["Red"] + max_blacks * scaled_chip_values["Black"])

    # Iterate over combinations of Blue and Green to satisfy constraints
    for blue_count in range(remaining_amount // scaled_chip_values["Blue"] + 1):
        for green_count in range(remaining_amount // scaled_chip_values["Green"] + 1):
            if blue_count * scaled_chip_values["Blue"] + green_count * scaled_chip_values["Green"] == remaining_amount and blue_count > green_count:
                chip_count["Blue"] = blue_count
                chip_count["Green"] = green_count
                remaining_amount = 0
                break
        if remaining_amount == 0:
            break

    # Final check
    if remaining_amount > 0:
        st.error("The chip distribution constraints could not be satisfied. Please adjust the buy-in amount or constraints.")

    # Scale back chip counts to original proportions
    chip_count = {color: int(count) for color, count in chip_count.items()}
    return chip_count

# Function to calculate the cash-out amount from chip counts
def calculate_cash_out(chip_counts, chip_values):
    total_amount = 0
    for color, count in chip_counts.items():
        total_amount += count * chip_values[color]
    return total_amount

# Streamlit app
def main():
    # Chip values as constants
    chip_values = {
        "Black": 2,
        "Green": 1,
        "Blue": 0.5,
        "Red": 0.2,
        "White": 0.1
    }

    # Fixed number of White, Red, and Black chips per buy-in
    min_whites = 15
    min_reds = 15
    max_blacks = 3

    # Sidebar navigation
    page = st.sidebar.radio("Navigate", ["Buy-In", "Cash Out"])

    if page == "Buy-In":
        st.title("Buy-In Calculator")
        st.write("Enter the buy-in amount and calculate the required chips.")

        # Input buy-in amount
        buy_in = st.number_input("Buy-In Amount:", min_value=1, value=20, key="buy_in")
        if st.button("Calculate Buy-In"):
            chip_distribution = calculate_chips(buy_in, chip_values, min_whites, min_reds, max_blacks)

            # Display chip results
            st.subheader("Chip Distribution")
            for color, count in chip_distribution.items():
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <div style="width: 30px; height: 30px; border-radius: 50%; background-color: {color.lower()}; margin-right: 10px;"></div>
                        <span style="flex: 1;">{color} chip ({chip_values[color]})</span>
                        <div style="padding: 5px; border: 1px solid #ccc; border-radius: 5px; width: 50px; text-align: center;">
                            {int(count)}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("**[Click to Buy-In](https://venmo.com/code?user_id=2485933647593472041&created=1736959326)**")

    elif page == "Cash Out":
        st.title("Cash-Out Calculator")
        st.write("Enter the number of chips to calculate the cash-out amount.")

        # Input chip counts
        chip_counts = {}
        for color in chip_values:
            chip_counts[color] = int(st.number_input(f"Number of {color} chips:", min_value=0, value=0, key=f"chip_{color}"))

        if st.button("Calculate Cash Out"):
            cash_out_amount = calculate_cash_out(chip_counts, chip_values)

            # Display total cash-out amount
            st.subheader("Cash-Out Amount")
            st.write(f"Total: ${cash_out_amount:.2f}")

        st.markdown("**[Click to Cashout](https://venmo.com/code?user_id=2485933647593472041&created=1736959326)**")

if __name__ == "__main__":
    main()

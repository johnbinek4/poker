import streamlit as st

# Function to calculate poker chips required for a buy-in
def calculate_chips(amount, chip_values, min_whites, min_reds, max_blacks):
    chip_count = {color: 0 for color in chip_values}
    remaining_amount = int(amount)

    # Ensure minimum White and Red chips are allocated first
    chip_count["White"] = min_whites
    chip_count["Red"] = min_reds
    remaining_amount -= int(min_whites * chip_values["White"] + min_reds * chip_values["Red"])

    # Allocate Black chips with a maximum limit per player
    max_black_value = int(max_blacks * chip_values["Black"])
    black_allocation = min(max_black_value, remaining_amount // chip_values["Black"] * chip_values["Black"])
    chip_count["Black"] = black_allocation // chip_values["Black"]
    remaining_amount -= black_allocation

    # Distribute remaining amount proportionally to other chips, ensuring more Blues than Greens
    while remaining_amount > 0:
        for color, value in sorted(chip_values.items(), key=lambda x: x[1], reverse=True):
            if color in ["White", "Red", "Black"]:
                continue  # Skip already allocated chips
            if value == 0:  # Prevent division by zero
                continue
            if color == "Blue":
                count = min(remaining_amount // value, 2)  # Distribute more Blues
            else:
                count = min(remaining_amount // value, 1)
            if count > 0:
                chip_count[color] += count
                remaining_amount -= count * value

    if remaining_amount > 0:
        st.warning("The amount cannot be exactly fulfilled with the given chip values.")

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

    # Minimum number of White and Red chips per buy-in
    min_whites = 15
    min_reds = 15
    max_blacks = 2  # Maximum number of Black chips per player

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
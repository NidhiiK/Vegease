# def format_notification_table(products):
#     table_html = """
#     <table border="1">
#         <tr>
#             <th style="padding: 10px;">Product Name</th>
#             <th style="padding: 10px;">Original Price</th>
#             <th style="padding: 10px;">Discounted Price</th>
#             <th style="padding: 10px;">Discount</th>
#         </tr>
#     """

#     for product in products:
#         product_name, original_price, discounted_price, discount = product
#         table_html += f"""
#         <tr>
#             <td style="padding: 5px;">{product_name}</td>
#             <td style="padding: 5px;">{original_price}</td>
#             <td style="padding: 5px;">{discounted_price}</td>
#             <td style="padding: 5px;">{discount}</td>
#         </tr>
#         """

#     table_html += "</table>"
#     return table_html



def format_notification_table(products):
    table_html = """
    <table border="1">
        <tr>
            <th style="padding: 10px;">Product Name</th>
            <th style="padding: 10px;">Previous Price</th>
            <th style="padding: 10px;">New Price</th>
            <th style="padding: 10px;">Quantity</th>
        </tr>
    """

    for product in products:
        product_name, original_price, discounted_price, quantity = product
        table_html += f"""
        <tr>
            <td style="padding: 5px;">{product_name}</td>
            <td style="padding: 5px;">{original_price}</td>
            <td style="padding: 5px;">{discounted_price}</td>
            <td style="padding: 5px;">{quantity}</td>
        </tr>
        """

    table_html += "</table>"
    return table_html

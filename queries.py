# pylint:disable=C0111,C0103
def order_rank_per_customer(db):
    query = """
    SELECT OrderID, CustomerID, OrderDate,
    RANK() OVER (PARTITION BY CustomerID ORDER BY OrderDate) AS OrderRank
    FROM Orders
    ORDER BY CustomerID, OrderDate;
    """
    db.execute(query)
    return db.fetchall()
def order_cumulative_amount_per_customer(db):
    query = """
    WITH OrderTotal AS (
        SELECT O.OrderID, O.CustomerID, O.OrderDate,
        SUM(OD.Quantity * OD.UnitPrice) AS TotalOrderAmount
        FROM Orders O
        JOIN OrderDetails OD ON O.OrderID = OD.OrderID
        GROUP BY O.OrderID, O.CustomerID, O.OrderDate
    )
    SELECT OrderID, CustomerID, OrderDate,
           SUM(TotalOrderAmount) OVER (
               PARTITION BY CustomerID ORDER BY OrderDate
           ) AS OrderCumulativeAmount
    FROM OrderTotal
    ORDER BY CustomerID, OrderDate
    """
    db.execute(query)
    return db.fetchall()

from flask import jsonify
from sqlalchemy import text
from app.db import engine

def register_routes(app):

    @app.route("/")
    def home():
        return jsonify({
            "message": "Welcome to LogiMigrate API",
            "status": "running"
        })

    @app.route("/summary")
    def get_summary():
        query = text("""
            SELECT 'products' AS table_name, COUNT(*) AS row_count FROM products
            UNION ALL
            SELECT 'warehouses', COUNT(*) FROM warehouses
            UNION ALL
            SELECT 'inventory', COUNT(*) FROM inventory
            UNION ALL
            SELECT 'demand', COUNT(*) FROM demand
            UNION ALL
            SELECT 'operations', COUNT(*) FROM operations;
        """)

        with engine.connect() as conn:
            result = conn.execute(query)
            summary = [
                {"table_name": row[0], "row_count": row[1]}
                for row in result
            ]

        return jsonify(summary)
    
    @app.route("/inventory/low-stock")
    def get_low_stock_items():
        query = text("""
            SELECT inventory_id, item_id, warehouse_id, stock_level, reorder_point
            FROM inventory
            WHERE stock_level < reorder_point
            ORDER BY stock_level ASC;
        """)

        with engine.connect() as conn:
            result = conn.execute(query)
            low_stock_items = [
                {
                    "inventory_id": row[0],
                    "item_id": row[1],
                    "warehouse_id": row[2],
                    "stock_level": row[3],
                    "reorder_point": row[4]
                }
                for row in result
            ]

        return jsonify(low_stock_items)

    @app.route("/inventory/low-stock/count")
    def get_low_stock_count():
        query = text("""
            SELECT COUNT(*) AS low_stock_count
            FROM inventory
            WHERE stock_level < reorder_point;
        """)

        with engine.connect() as conn:
            result = conn.execute(query).fetchone()

        return jsonify({
            "low_stock_count": result[0]
        })

    @app.route("/operations/summary")
    def get_operations_summary():
        query = text("""
            SELECT 
                AVG(order_fulfillment_rate) AS avg_fulfillment_rate,
                AVG("KPI_score") AS avg_kpi_score,
                AVG(picking_time_seconds) AS avg_picking_time
            FROM operations;
        """)

        with engine.connect() as conn:
            result = conn.execute(query).fetchone()

        return jsonify({
            "avg_fulfillment_rate": round(result[0], 4),
            "avg_kpi_score": round(result[1], 4),
            "avg_picking_time_seconds": round(result[2], 2)
        })

    @app.route("/products/<item_id>")
    def get_product_by_id(item_id):
        query = text("""
            SELECT item_id, category, unit_price, handling_cost_per_unit,
                holding_cost_per_unit_day, item_popularity_score
            FROM products
            WHERE item_id = :item_id;
        """)

        with engine.connect() as conn:
            result = conn.execute(query, {"item_id": item_id}).fetchone()

        if result is None:
            return jsonify({"error": "Product not found"}), 404

        return jsonify({
            "item_id": result[0],
            "category": result[1],
            "unit_price": result[2],
            "handling_cost_per_unit": result[3],
            "holding_cost_per_unit_day": result[4],
            "item_popularity_score": result[5]
        })

    @app.route("/inventory/low-stock/details")
    def get_low_stock_details():
        query = text("""
            SELECT 
                i.inventory_id,
                i.item_id,
                p.category,
                p.unit_price,
                i.warehouse_id,
                i.stock_level,
                i.reorder_point
            FROM inventory i
            JOIN products p
                ON i.item_id = p.item_id
            WHERE i.stock_level < i.reorder_point
            ORDER BY i.stock_level ASC;
        """)

        with engine.connect() as conn:
            result = conn.execute(query)

            low_stock_details = [
                {
                    "inventory_id": row[0],
                    "item_id": row[1],
                    "category": row[2],
                    "unit_price": row[3],
                    "warehouse_id": row[4],
                    "stock_level": row[5],
                    "reorder_point": row[6]
                }
                for row in result
            ]

        return jsonify(low_stock_details)

    @app.route("/demand/<item_id>")
    def get_demand_by_item(item_id):
        query = text("""
            SELECT 
                demand_id,
                item_id,
                daily_demand,
                demand_std_dev,
                forecasted_demand_next_7d,
                total_orders_last_month
            FROM demand
            WHERE item_id = :item_id;
        """)

        with engine.connect() as conn:
            result = conn.execute(query, {"item_id": item_id}).fetchone()

        if result is None:
            return jsonify({"error": "Demand record not found"}), 404

        return jsonify({
            "demand_id": result[0],
            "item_id": result[1],
            "daily_demand": result[2],
            "demand_std_dev": result[3],
            "forecasted_demand_next_7d": result[4],
            "total_orders_last_month": result[5]
        })
        
    @app.route("/migration/health")
    def get_migration_health():
        query = text("""
            SELECT
                (SELECT COUNT(*) FROM products) AS total_products,
                (SELECT COUNT(*) FROM warehouses) AS total_warehouses,
                (SELECT COUNT(*) FROM inventory) AS total_inventory_records,
                (SELECT COUNT(*) FROM demand) AS total_demand_records,
                (SELECT COUNT(*) FROM operations) AS total_operations_records,
                (SELECT COUNT(*) FROM inventory WHERE stock_level < reorder_point) AS low_stock_count,
                (SELECT AVG(order_fulfillment_rate) FROM operations) AS avg_fulfillment_rate,
                (SELECT AVG("KPI_score") FROM operations) AS avg_kpi_score;
        """)

        with engine.connect() as conn:
            result = conn.execute(query).fetchone()

        return jsonify({
            "total_products": result[0],
            "total_warehouses": result[1],
            "total_inventory_records": result[2],
            "total_demand_records": result[3],
            "total_operations_records": result[4],
            "low_stock_count": result[5],
            "avg_fulfillment_rate": round(result[6], 4),
            "avg_kpi_score": round(result[7], 4)
        })
        
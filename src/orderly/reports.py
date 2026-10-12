"""Orderly — report computation module.

This is a brownfield project: some functions are complete, some are
TODO-marked gaps, and one has a planted bug. Work through TASKS.md.
"""

from __future__ import annotations

import csv
import logging
import time

logger = logging.getLogger("orderly.reports")


# --------------------------------------------------------------------------
# Task T1 — planted bug (see TASKS.md)
# --------------------------------------------------------------------------
def monthly_revenue(conn):
    
    rows = conn.execute(
        """
        SELECT strftime('%Y-%m', o.order_date) AS month,
               SUM(oi.qty * oi.unit_price) AS revenue
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.id
        WHERE o.status = 'completed'
        GROUP BY month
        ORDER BY month
        """
        
        
    ).fetchall()
    return [(m, round(r, 2)) for m, r in rows]


# --------------------------------------------------------------------------
# Task T2 — TODO gaps
# --------------------------------------------------------------------------
def monthly_running_total(conn):
    """Return [(month, revenue, running_total), ...] sorted by month.

    Build on monthly_revenue(); do not re-query the database here.
    """
    running = 0.0
    result = []
    for month, revenue in monthly_revenue(conn):
        running = round(running + revenue, 2)
        result.append((month, revenue, running))
    return result


def top_customers(conn, limit=5):
    """Return [(name, city, revenue), ...] for the top `limit` customers by
    total revenue (completed orders only), highest revenue first.
    """
    rows = conn.execute(
        """
        SELECT c.name, c.city, SUM(oi.qty * oi.unit_price) AS revenue
        FROM customers c
        JOIN orders o ON o.customer_id = c.id
        JOIN order_items oi ON oi.order_id = o.id
        WHERE o.status = 'completed'
        GROUP BY c.id, c.name, c.city
        ORDER BY revenue DESC, c.name ASC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    return [(name, city, round(revenue, 2)) for name, city, revenue in rows]


def iter_completed_items(conn):
    """Yield one dict per order item belonging to a completed order.

    Keys: order_id, month, product, category, qty, unit_price, amount.
    Must be a generator (use yield).
    """
    rows = conn.execute(
        """
        SELECT o.id, strftime('%Y-%m', o.order_date), p.name, p.category,
               oi.qty, oi.unit_price
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.id
        JOIN products p ON p.id = oi.product_id
        WHERE o.status = 'completed'
        ORDER BY oi.id
        """
    )
    for order_id, month, product, category, qty, unit_price in rows:
        yield {
            "order_id": order_id,
            "month": month,
            "product": product,
            "category": category,
            "qty": qty,
            "unit_price": unit_price,
            "amount": round(qty * unit_price, 2),
        }


class SalesSummary:
    """A small container for monthly revenue rows.

    TODO(T2d): implement this class.
      - constructor takes a list of (month, revenue) tuples
      - len(summary)            -> number of months
      - repr(summary)           -> "SalesSummary(months=4, total=12345.67)"
      - summary.total_revenue   -> property, sum of revenues (2 decimals)
      - summary.best_month()    -> (month, revenue) of the best month
    """

    def __init__(self, rows):
        self.rows = list(rows)

    def __len__(self):
        return len(self.rows)

    @property
    def total_revenue(self):
        return round(sum(revenue for _, revenue in self.rows), 2)

    def __repr__(self):
        return f"SalesSummary(months={len(self)}, total={self.total_revenue:.2f})"

    def best_month(self):
        return max(self.rows, key=lambda row: row[1]) if self.rows else None


def timed(func):
    """Decorator: log "<funcname> took <ms> ms" at INFO level and return the
    wrapped function's result unchanged.

    TODO(T2e): implement. Use the module logger and time.perf_counter().
    """
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000
            logger.info("%s took %.2f ms", func.__name__, elapsed_ms)

    return wrapper


def write_report(rows, out_path, header):
    """Write `rows` (a list of tuples) to `out_path` as CSV with `header`.

    TODO(T2f): implement.
      - create the parent directory if it does not exist
      - raise ValueError("no rows to write") when rows is empty
      - use a context manager for the file and newline=""
      - log how many rows were written (INFO level)
      - return the path written (as str)
    """
    if not rows:
        raise ValueError("no rows to write")
    from pathlib import Path

    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        writer.writerows(rows)
    logger.info("Wrote %d rows to %s", len(rows), path)
    return str(path)


# --------------------------------------------------------------------------
# Completed reference code (do not edit)
# --------------------------------------------------------------------------
def revenue_by_category(conn):
    """Return [(category, revenue), ...] for completed orders, highest first."""
    rows = conn.execute(
        """
        SELECT p.category, SUM(oi.qty * oi.unit_price) AS revenue
        FROM order_items oi
        JOIN orders   o ON o.id = oi.order_id
        JOIN products p ON p.id = oi.product_id
        WHERE o.status = 'completed'
        GROUP BY p.category
        ORDER BY revenue DESC
        """
    ).fetchall()
    return [(c, round(r, 2)) for c, r in rows]

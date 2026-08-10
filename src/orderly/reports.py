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
    """Return [(month, revenue), ...] sorted ascending by month.

    Revenue = SUM(qty * unit_price) over order items whose order status is
    'completed'. Month is 'YYYY-MM' taken from the order date.

    NOTE(top-customers): status filter added on this branch; the
    top-customers report expects completed-only revenue.
    """
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
    # TODO(T2a): implement using monthly_revenue(conn) and accumulate the
    # running total. Round every money value to 2 decimals.
    raise NotImplementedError("TODO(T2a): monthly_running_total")


def top_customers(conn, limit=5):
    """Return [(name, city, revenue), ...] for the top `limit` customers by
    total revenue (completed orders only), highest revenue first.
    """
    # TODO(T2b): implement with a JOIN + GROUP BY + ORDER BY + LIMIT query.
    # Round revenue to 2 decimals.
    raise NotImplementedError("TODO(T2b): top_customers")


def iter_completed_items(conn):
    """Yield one dict per order item belonging to a completed order.

    Keys: order_id, month, product, category, qty, unit_price, amount.
    Must be a generator (use yield).
    """
    # TODO(T2c): implement as a generator.
    raise NotImplementedError("TODO(T2c): iter_completed_items")


class SalesSummary:
    """A small container for monthly revenue rows.

    TODO(T2d): implement this class.
      - constructor takes a list of (month, revenue) tuples
      - len(summary)            -> number of months
      - repr(summary)           -> "SalesSummary(months=4, total=12345.67)"
      - summary.total_revenue   -> property, sum of revenues (2 decimals)
      - summary.best_month()    -> (month, revenue) of the best month
    """

    # TODO(T2d): implement the class described above.
    pass


def timed(func):
    """Decorator: log "<funcname> took <ms> ms" at INFO level and return the
    wrapped function's result unchanged.

    TODO(T2e): implement. Use the module logger and time.perf_counter().
    """
    # TODO(T2e): implement the decorator.
    raise NotImplementedError("TODO(T2e): timed")


def write_report(rows, out_path, header):
    """Write `rows` (a list of tuples) to `out_path` as CSV with `header`.

    TODO(T2f): implement.
      - create the parent directory if it does not exist
      - raise ValueError("no rows to write") when rows is empty
      - use a context manager for the file and newline=""
      - log how many rows were written (INFO level)
      - return the path written (as str)
    """
    # TODO(T2f): implement write_report.
    raise NotImplementedError("TODO(T2f): write_report")


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

import csv
import json
from abc import ABC, abstractmethod
from storage.db import load_entries
from utils.builders import ResponseBuilder
from pathlib import Path

EXPORT_DIR = Path("data/exports")

class Exporter(ABC):
    @abstractmethod
    def export(self, entries: list, filepath: Path):
        pass

class JSONExporter(Exporter):
    def export(self, entries: list, filepath: Path):
        with open(filepath, "w") as f:
            json.dump(entries, f, indent=2)

class CSVExporter(Exporter):
    def export(self, entries: list, filepath: Path):
        if not entries:
            raise ValueError("No entries to export")
        
        keys = entries[0].keys()
        with open(filepath, "w", newline='') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(entries)

class ExporterFactory:
    @staticmethod
    def get_exporter(format: str) -> Exporter:
        if format == "json":
            return JSONExporter()
        elif format == "csv":
            return CSVExporter()
        raise ValueError(f"Unsupported format: {format}")

def export_data(format: str = "csv"):
    """
    Export all mood data using Factory Pattern.
    Format can be 'csv' or 'json'.
    Optimized for AI agent consumption.
    """
    if not EXPORT_DIR.exists():
        EXPORT_DIR.mkdir(parents=True)
        
    entries = load_entries()
    if not entries:
        return ResponseBuilder.error("No data to export")

    try:
        exporter = ExporterFactory.get_exporter(format)
        filename = f"mood_export_{format}.{format}"
        filepath = EXPORT_DIR / filename
        
        exporter.export(entries, filepath)

        return ResponseBuilder.success(
            f"Data exported successfully to {filepath}", 
            {"filepath": str(filepath.absolute()), "entries_count": len(entries)}
        )
    except ValueError as e:
        return ResponseBuilder.error(str(e))
    except Exception as e:
        return ResponseBuilder.error(f"Failed to export data: {str(e)}")

import asyncio
import logging
import time
from services.parsers.file_router import ParseRouter
from detectors.column_detector import ColumnDetector
from mappers.column_mapper import ColumnMaper
from schemas.target_schema import AmazonProductSchema
from validators.data_validator import DataValidator
from transformers.data_transformer import DataTransformer
from output.output_writer import OutputWriter
from audit.audit_logger import AuditLogger

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)


async def main():
    source_file = "E:\\SmartCleansing\\airports.json"
    start = time.time()

    router = ParseRouter(source_file, chunk_size=100)
    parser = router.get_parser()
    target_fields = list(AmazonProductSchema.model_fields.keys())

    async for batch in parser.parse():
        # detect
        stats = ColumnDetector(batch).analyze_col()

        # map
        mapping = ColumnMaper(
            detected_columns=stats,
            target_schema=target_fields
        ).map_rules()

        # validate
        result = DataValidator(
            batch=batch,
            mapping=mapping
        ).validate()

        # transform
        transformed = DataTransformer(result['valid']).transform()

        # output
        await OutputWriter(transformed).write()

        # audit
        duration = round(time.time() - start, 3)
        await AuditLogger(
            source_file=source_file,
            total_rows=len(batch),
            valid_rows=len(result['valid']),
            invalid_rows=len(result['invalid']),
            mapping=mapping,
            duration_seconds=duration
        ).log()

        print(f"\n{'='*50}")
        print(f"Valid rows   : {len(result['valid'])}")
        print(f"Invalid rows : {len(result['invalid'])}")
        print(f"Duration     : {duration}s")


if __name__ == "__main__":
    asyncio.run(main())
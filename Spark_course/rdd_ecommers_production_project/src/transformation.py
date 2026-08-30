def format_parsing_rejects(record):
    status = record[0]
    row_data = record[1]
    error_reason = record[2]
    
    return(
        "Parsing",
        row_data,
        error_reason
    )
    
def format_validation_rejects(record):
    status = record[0]
    row_data = record[1]
    error_reason = record[2]
    
    return(
        "Validation",
        row_data,
        error_reason
    )
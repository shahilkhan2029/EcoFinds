<?php
function updatePropertyStatus($conn, $property_id, $status) {
    // Validate inputs
    if (!is_numeric($property_id) || !in_array($status, ['available', 'sold', 'rented'])) {
        return false;
    }

    try {
        // Prepare the SQL statement
        $sql = "UPDATE properties SET status = ?, updated_at = NOW() WHERE id = ?";
        $stmt = mysqli_prepare($conn, $sql);
        
        if (!$stmt) {
            error_log("Error preparing statement: " . mysqli_error($conn));
            return false;
        }

        // Bind parameters
        if (!mysqli_stmt_bind_param($stmt, "si", $status, $property_id)) {
            error_log("Error binding parameters: " . mysqli_stmt_error($stmt));
            mysqli_stmt_close($stmt);
            return false;
        }

        // Execute the statement
        if (!mysqli_stmt_execute($stmt)) {
            error_log("Error executing statement: " . mysqli_stmt_error($stmt));
            mysqli_stmt_close($stmt);
            return false;
        }

        // Check if any rows were affected
        $affected_rows = mysqli_stmt_affected_rows($stmt);
        mysqli_stmt_close($stmt);

        return $affected_rows > 0;
    } catch (Exception $e) {
        error_log("Exception in updatePropertyStatus: " . $e->getMessage());
        return false;
    }
}
?> 
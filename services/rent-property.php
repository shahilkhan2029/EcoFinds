<?php
require_once "../config.php";

$success_msg = $error_msg = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get form data
    $name = trim($_POST["name"]);
    $email = trim($_POST["email"]);
    $phone = trim($_POST["phone"]);
    $preferred_location = trim($_POST["preferred_location"]);
    $property_type = trim($_POST["property_type"]);
    $budget = trim($_POST["budget"]);
    $move_in_date = trim($_POST["move_in_date"]);
    $requirements = trim($_POST["requirements"]);

    // Insert into database
    $sql = "INSERT INTO rental_inquiries (name, email, phone, preferred_location, property_type, budget, move_in_date, requirements, status) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Pending')";
    
    if($stmt = mysqli_prepare($conn, $sql)){
        mysqli_stmt_bind_param($stmt, "sssssdss", 
            $name, $email, $phone, $preferred_location, 
            $property_type, $budget, $move_in_date, $requirements);
        
        if(mysqli_stmt_execute($stmt)){
            $success_msg = "Your rental inquiry has been submitted successfully! Our team will contact you within 24 hours.";
        } else{
            $error_msg = "Error submitting inquiry. Please try again.";
        }
        mysqli_stmt_close($stmt);
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rent a Property | PrimeHomes</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Arial', sans-serif;
        }

        body {
            background-color: #f5f5f5;
        }

        /* Header Styles */
        .main-header {
            background-color: white;
            padding: 20px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        .main-header-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
            color: #2c3e50;
        }

        .logo i {
            font-size: 24px;
            color: #007bff;
        }

        .logo h1 {
            font-size: 24px;
            font-weight: bold;
            color: #FF6B6B;
        }

        .main-nav {
            display: flex;
            gap: 40px;
            align-items: center;
        }

        .nav-link {
            text-decoration: none;
            color: #2c3e50;
            font-weight: 500;
            padding: 8px 0;
            position: relative;
            transition: color 0.3s ease;
        }

        .nav-link:hover {
            color: #007bff;
        }

        .nav-link::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 0;
            height: 2px;
            background-color: #007bff;
            transition: width 0.3s ease;
        }

        .nav-link:hover::after,
        .nav-link.active::after {
            width: 100%;
        }

        .nav-link.active {
            color: #007bff;
        }

        .dropdown-btn {
            text-decoration: none;
            color: white;
            font-weight: 500;
            padding: 8px 15px;
            background: #007bff;
            border-radius: 4px;
            display: flex;
            align-items: center;
            gap: 5px;
            transition: all 0.3s ease;
        }

        .dropdown-btn:hover {
            background: #0056b3;
        }

        /* Main Content Styles */
        .container {
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 20px;
        }

        .service-header {
            text-align: center;
            margin-bottom: 40px;
        }

        .service-header h2 {
            font-size: 2.5rem;
            color: #2c3e50;
            margin-bottom: 15px;
        }

        .service-header p {
            color: #666;
            font-size: 1.1rem;
            max-width: 800px;
            margin: 0 auto;
        }

        .benefits-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin: 60px 0;
        }

        .benefit-card {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            text-align: center;
        }

        .benefit-card i {
            font-size: 40px;
            color: #007bff;
            margin-bottom: 20px;
        }

        .benefit-card h3 {
            color: #2c3e50;
            margin-bottom: 15px;
        }

        .benefit-card p {
            color: #666;
            line-height: 1.6;
        }

        .rental-form {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 5px;
            color: #2c3e50;
            font-weight: 500;
        }

        .form-control {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }

        .form-control:focus {
            outline: none;
            border-color: #007bff;
        }

        textarea.form-control {
            height: 120px;
            resize: vertical;
        }

        .submit-btn {
            background: #007bff;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
            transition: background 0.3s ease;
        }

        .submit-btn:hover {
            background: #0056b3;
        }

        .alert {
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 4px;
        }

        .alert-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .alert-danger {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .process-steps {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            margin: 60px 0;
        }

        .step-card {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            text-align: center;
            position: relative;
        }

        .step-number {
            position: absolute;
            top: -15px;
            left: 50%;
            transform: translateX(-50%);
            background: #007bff;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }

        .step-card i {
            font-size: 40px;
            color: #007bff;
            margin: 20px 0;
        }

        .step-card h3 {
            color: #2c3e50;
            margin-bottom: 15px;
        }

        .step-card p {
            color: #666;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header class="main-header">
        <div class="main-header-content">
            <a href="../index.php" class="logo">
                <i class="fas fa-home"></i>
                <h1>PrimeHomes</h1>
            </a>
            <nav class="main-nav">
                <a href="../index.php" class="nav-link">Home</a>
                <a href="../rent.php" class="nav-link">Rent</a>
                <a href="../sell.php" class="nav-link">Sell</a>
                <a href="../contact.php" class="nav-link">Contact</a>
                <a href="../add-property.php" class="dropdown-btn">
                    <i class="fas fa-plus"></i> Add Property
                </a>
            </nav>
        </div>
    </header>

    <div class="container">
        <div class="service-header">
            <h2>Rent a Property</h2>
            <p>Find your perfect rental home with PrimeHomes. We offer a wide range of properties to suit your needs and budget.</p>
        </div>

        <div class="benefits-grid">
            <div class="benefit-card">
                <i class="fas fa-search"></i>
                <h3>Wide Selection</h3>
                <p>Access to thousands of verified rental properties across prime locations.</p>
            </div>
            <div class="benefit-card">
                <i class="fas fa-shield-alt"></i>
                <h3>Verified Listings</h3>
                <p>All properties are thoroughly verified to ensure your safety and security.</p>
            </div>
            <div class="benefit-card">
                <i class="fas fa-hand-holding-usd"></i>
                <h3>Best Deals</h3>
                <p>Competitive rental rates and transparent pricing with no hidden charges.</p>
            </div>
        </div>

        <div class="process-steps">
            <div class="step-card">
                <div class="step-number">1</div>
                <i class="fas fa-clipboard-list"></i>
                <h3>Submit Inquiry</h3>
                <p>Fill out our rental inquiry form with your requirements and preferences.</p>
            </div>
            <div class="step-card">
                <div class="step-number">2</div>
                <i class="fas fa-home"></i>
                <h3>Property Viewing</h3>
                <p>Schedule viewings of properties that match your criteria.</p>
            </div>
            <div class="step-card">
                <div class="step-number">3</div>
                <i class="fas fa-file-signature"></i>
                <h3>Documentation</h3>
                <p>Complete the rental agreement and necessary documentation.</p>
            </div>
            <div class="step-card">
                <div class="step-number">4</div>
                <i class="fas fa-key"></i>
                <h3>Move In</h3>
                <p>Get your keys and move into your new rental home.</p>
            </div>
        </div>

        <div class="rental-form">
            <h3 style="text-align: center; margin-bottom: 30px; color: #2c3e50;">Submit Rental Inquiry</h3>
            
            <?php 
            if(!empty($success_msg)){
                echo '<div class="alert alert-success">' . $success_msg . '</div>';
            }
            if(!empty($error_msg)){
                echo '<div class="alert alert-danger">' . $error_msg . '</div>';
            }
            ?>

            <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="POST">
                <div class="form-group">
                    <label>Full Name</label>
                    <input type="text" name="name" class="form-control" required>
                </div>

                <div class="form-group">
                    <label>Email Address</label>
                    <input type="email" name="email" class="form-control" required>
                </div>

                <div class="form-group">
                    <label>Phone Number</label>
                    <input type="tel" name="phone" class="form-control" required>
                </div>

                <div class="form-group">
                    <label>Preferred Location</label>
                    <input type="text" name="preferred_location" class="form-control" required>
                </div>

                <div class="form-group">
                    <label>Property Type</label>
                    <select name="property_type" class="form-control" required>
                        <option value="">Select Property Type</option>
                        <option value="apartment">Apartment</option>
                        <option value="house">House</option>
                        <option value="villa">Villa</option>
                        <option value="studio">Studio</option>
                        <option value="penthouse">Penthouse</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Monthly Budget (₹)</label>
                    <input type="number" name="budget" class="form-control" required min="0" step="1000">
                </div>

                <div class="form-group">
                    <label>Preferred Move-in Date</label>
                    <input type="date" name="move_in_date" class="form-control" required min="<?php echo date('Y-m-d'); ?>">
                </div>

                <div class="form-group">
                    <label>Additional Requirements</label>
                    <textarea name="requirements" class="form-control" placeholder="Please specify any additional requirements (e.g., furnished, parking, pet-friendly)..."></textarea>
                </div>

                <button type="submit" class="submit-btn">Submit Inquiry</button>
            </form>
        </div>
    </div>
</body>
</html> 
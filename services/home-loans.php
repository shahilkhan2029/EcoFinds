<?php
require_once "../config.php";

$success_msg = $error_msg = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get form data
    $name = trim($_POST["name"]);
    $email = trim($_POST["email"]);
    $phone = trim($_POST["phone"]);
    $property_address = trim($_POST["property_address"]);
    $loan_amount = trim($_POST["loan_amount"]);
    $employment_status = trim($_POST["employment_status"]);
    $monthly_income = trim($_POST["monthly_income"]);
    $credit_score = trim($_POST["credit_score"]);
    $additional_info = trim($_POST["additional_info"]);

    // Insert into database
    $sql = "INSERT INTO loan_applications (name, email, phone, property_address, loan_amount, employment_status, monthly_income, credit_score, additional_info, status) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pending')";
    
    if($stmt = mysqli_prepare($conn, $sql)){
        mysqli_stmt_bind_param($stmt, "ssssdsdis", 
            $name, $email, $phone, $property_address, 
            $loan_amount, $employment_status, $monthly_income, 
            $credit_score, $additional_info);
        
        if(mysqli_stmt_execute($stmt)){
            $success_msg = "Your loan application has been submitted successfully! Our team will contact you within 24 hours.";
        } else{
            $error_msg = "Error submitting application. Please try again.";
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
    <title>Home Loans | PrimeHomes</title>
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

        .loan-form {
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

        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 60px;
        }

        .feature-card {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            text-align: center;
        }

        .feature-card i {
            font-size: 40px;
            color: #007bff;
            margin-bottom: 20px;
        }

        .feature-card h3 {
            color: #2c3e50;
            margin-bottom: 15px;
        }

        .feature-card p {
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
            <h2>Home Loans</h2>
            <p>Get the best home loan rates and terms from our trusted financial partners. We'll help you find the perfect mortgage solution for your dream home.</p>
        </div>

        <div class="features">
            <div class="feature-card">
                <i class="fas fa-percentage"></i>
                <h3>Competitive Rates</h3>
                <p>Access to exclusive mortgage rates from our network of trusted lenders.</p>
            </div>
            <div class="feature-card">
                <i class="fas fa-clock"></i>
                <h3>Quick Approval</h3>
                <p>Fast and efficient loan processing with minimal documentation.</p>
            </div>
            <div class="feature-card">
                <i class="fas fa-hand-holding-usd"></i>
                <h3>Flexible Terms</h3>
                <p>Customizable loan terms to suit your financial situation and goals.</p>
            </div>
        </div>

        <div class="loan-form">
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
                    <label>Property Address</label>
                    <input type="text" name="property_address" class="form-control" required>
                </div>

                <div class="form-group">
                    <label>Loan Amount (USD)</label>
                    <input type="number" name="loan_amount" class="form-control" required min="0" step="1000">
                </div>

                <div class="form-group">
                    <label>Employment Status</label>
                    <select name="employment_status" class="form-control" required>
                        <option value="">Select Employment Status</option>
                        <option value="employed">Employed</option>
                        <option value="self-employed">Self-Employed</option>
                        <option value="retired">Retired</option>
                        <option value="unemployed">Unemployed</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Monthly Income (USD)</label>
                    <input type="number" name="monthly_income" class="form-control" required min="0" step="100">
                </div>

                <div class="form-group">
                    <label>Credit Score</label>
                    <input type="number" name="credit_score" class="form-control" required min="300" max="850">
                </div>

                <div class="form-group">
                    <label>Additional Information</label>
                    <textarea name="additional_info" class="form-control" placeholder="Please provide any additional information about your financial situation..."></textarea>
                </div>

                <button type="submit" class="submit-btn">Submit Application</button>
            </form>
        </div>
    </div>
</body>
</html> 
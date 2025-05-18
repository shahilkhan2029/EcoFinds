// Email utility functions
class EmailService {
    constructor(config) {
        this.config = config;
    }

    async sendEmail(to, subject, message, options = {}) {
        try {
            const response = await fetch('/api/email/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    to,
                    subject,
                    message,
                    ...options
                })
            });

            if (!response.ok) {
                throw new Error('Failed to send email');
            }

            return await response.json();
        } catch (error) {
            console.error('Error sending email:', error);
            throw error;
        }
    }

    async sendContactForm(data) {
        return this.sendEmail(
            this.config.from,
            'New Contact Form Submission',
            `
                Name: ${data.name}
                Email: ${data.email}
                Phone: ${data.phone}
                Subject: ${data.subject}
                Message: ${data.message}
            `,
            {
                replyTo: data.email
            }
        );
    }

    async sendPasswordReset(email, resetToken) {
        const resetUrl = `${this.config.baseUrl}/reset-password?token=${resetToken}`;
        return this.sendEmail(
            email,
            'Password Reset Request',
            `
                Hello,
                
                You have requested to reset your password. Please click the link below to reset your password:
                
                ${resetUrl}
                
                If you did not request this, please ignore this email.
                
                Best regards,
                PrimeHomes Team
            `
        );
    }

    async sendWelcomeEmail(email, name) {
        return this.sendEmail(
            email,
            'Welcome to PrimeHomes',
            `
                Hello ${name},
                
                Welcome to PrimeHomes! We're excited to have you on board.
                
                You can now:
                - Browse our properties
                - Save your favorite listings
                - Contact our agents
                - And much more!
                
                If you have any questions, feel free to contact us.
                
                Best regards,
                PrimeHomes Team
            `
        );
    }

    async sendPropertyInquiry(property, inquiry) {
        return this.sendEmail(
            property.agentEmail,
            `New Inquiry for ${property.title}`,
            `
                Hello ${property.agentName},
                
                You have received a new inquiry for your property "${property.title}".
                
                Inquiry Details:
                Name: ${inquiry.name}
                Email: ${inquiry.email}
                Phone: ${inquiry.phone}
                Message: ${inquiry.message}
                
                Property Details:
                Price: ${property.price}
                Location: ${property.location}
                Type: ${property.type}
                
                Please respond to this inquiry as soon as possible.
                
                Best regards,
                PrimeHomes Team
            `,
            {
                replyTo: inquiry.email
            }
        );
    }
}

// Export the email service
export default EmailService; 
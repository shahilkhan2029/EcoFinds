// Database utility functions
class DatabaseService {
    constructor(config) {
        this.config = config;
    }

    async query(endpoint, method = 'GET', data = null) {
        try {
            const options = {
                method,
                headers: {
                    'Content-Type': 'application/json',
                }
            };

            if (data) {
                options.body = JSON.stringify(data);
            }

            const response = await fetch(`/api/${endpoint}`, options);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Database query error:', error);
            throw error;
        }
    }

    // Property operations
    async getProperties(filters = {}) {
        return this.query('properties?' + new URLSearchParams(filters));
    }

    async getPropertyById(id) {
        return this.query(`properties/${id}`);
    }

    async createProperty(propertyData) {
        return this.query('properties', 'POST', propertyData);
    }

    async updateProperty(id, propertyData) {
        return this.query(`properties/${id}`, 'PUT', propertyData);
    }

    async deleteProperty(id) {
        return this.query(`properties/${id}`, 'DELETE');
    }

    // Agent operations
    async getAgents(filters = {}) {
        return this.query('agents?' + new URLSearchParams(filters));
    }

    async getAgentById(id) {
        return this.query(`agents/${id}`);
    }

    async createAgent(agentData) {
        return this.query('agents', 'POST', agentData);
    }

    async updateAgent(id, agentData) {
        return this.query(`agents/${id}`, 'PUT', agentData);
    }

    async deleteAgent(id) {
        return this.query(`agents/${id}`, 'DELETE');
    }

    // User operations
    async login(credentials) {
        return this.query('auth/login', 'POST', credentials);
    }

    async register(userData) {
        return this.query('auth/register', 'POST', userData);
    }

    async resetPassword(email) {
        return this.query('auth/reset-password', 'POST', { email });
    }

    async updateProfile(userId, profileData) {
        return this.query(`users/${userId}/profile`, 'PUT', profileData);
    }

    // Contact operations
    async submitContactForm(formData) {
        return this.query('contact', 'POST', formData);
    }

    async getContactMessages(filters = {}) {
        return this.query('contact?' + new URLSearchParams(filters));
    }

    // Search operations
    async searchProperties(query) {
        return this.query('search/properties?' + new URLSearchParams(query));
    }

    async searchAgents(query) {
        return this.query('search/agents?' + new URLSearchParams(query));
    }

    // File upload operations
    async uploadFile(file, type) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('type', type);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('File upload failed');
            }

            return await response.json();
        } catch (error) {
            console.error('File upload error:', error);
            throw error;
        }
    }
}

// Export the database service
export default DatabaseService; 
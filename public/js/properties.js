// Property Management
class PropertyManager {
    constructor() {
        this.properties = [];
        this.filters = {
            type: '',
            location: '',
            priceRange: '',
            propertyType: ''
        };
        this.init();
    }

    init() {
        // Load properties
        this.loadProperties();
        // Add event listeners
        this.addEventListeners();
    }

    addEventListeners() {
        // Search form submission
        const searchForm = document.querySelector('.search-box form');
        if (searchForm) {
            searchForm.addEventListener('submit', (e) => this.handleSearch(e));
        }

        // Filter changes
        const filterInputs = document.querySelectorAll('.filter-input');
        filterInputs.forEach(input => {
            input.addEventListener('change', () => this.applyFilters());
        });
    }

    async loadProperties() {
        try {
            // In a real application, this would be an API call
            // For now, we'll use mock data
            this.properties = await this.getMockProperties();
            this.displayProperties();
        } catch (error) {
            console.error('Error loading properties:', error);
        }
    }

    displayProperties(properties = this.properties) {
        const container = document.getElementById('featuredProperties');
        if (!container) return;

        container.innerHTML = properties.map(property => this.createPropertyCard(property)).join('');
    }

    createPropertyCard(property) {
        return `
            <div class="col-md-4 mb-4">
                <div class="card property-card">
                    <img src="${property.main_image}" class="card-img-top" alt="${property.title}">
                    <div class="card-body">
                        <h5 class="card-title">${property.title}</h5>
                        <p class="price">$${property.price.toLocaleString()}</p>
                        <p class="card-text">${property.description.substring(0, 100)}...</p>
                        <div class="features">
                            <span><i class="fas fa-bed"></i> ${property.bedrooms} Beds</span>
                            <span class="ms-3"><i class="fas fa-bath"></i> ${property.bathrooms} Baths</span>
                            <span class="ms-3"><i class="fas fa-ruler-combined"></i> ${property.area} sqft</span>
                        </div>
                        <a href="property-details.html?id=${property.id}" class="btn btn-primary mt-3">View Details</a>
                    </div>
                </div>
            </div>
        `;
    }

    handleSearch(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        this.filters = {
            location: formData.get('location') || '',
            type: formData.get('type') || '',
            priceRange: formData.get('priceRange') || '',
            propertyType: formData.get('propertyType') || ''
        };
        this.applyFilters();
    }

    applyFilters() {
        let filteredProperties = [...this.properties];

        if (this.filters.location) {
            filteredProperties = filteredProperties.filter(property =>
                property.location.toLowerCase().includes(this.filters.location.toLowerCase())
            );
        }

        if (this.filters.type) {
            filteredProperties = filteredProperties.filter(property =>
                property.type === this.filters.type
            );
        }

        if (this.filters.propertyType) {
            filteredProperties = filteredProperties.filter(property =>
                property.property_type === this.filters.propertyType
            );
        }

        if (this.filters.priceRange) {
            const [min, max] = this.filters.priceRange.split('-').map(price =>
                parseInt(price.replace(/[^0-9]/g, ''))
            );
            filteredProperties = filteredProperties.filter(property =>
                property.price >= min && property.price <= max
            );
        }

        this.displayProperties(filteredProperties);
    }

    // Mock data (replace with actual API calls)
    async getMockProperties() {
        return [
            {
                id: 1,
                title: 'Modern Apartment in Downtown',
                type: 'rent',
                price: 2500,
                location: 'Downtown',
                bedrooms: 2,
                bathrooms: 2,
                area: 1200,
                description: 'Beautiful modern apartment with stunning city views.',
                main_image: 'images/property1.jpg',
                property_type: 'apartment'
            },
            {
                id: 2,
                title: 'Luxury Villa with Pool',
                type: 'sell',
                price: 750000,
                location: 'Suburbs',
                bedrooms: 4,
                bathrooms: 3,
                area: 3000,
                description: 'Spacious luxury villa with private pool and garden.',
                main_image: 'images/property2.jpg',
                property_type: 'villa'
            },
            {
                id: 3,
                title: 'Cozy Family Home',
                type: 'sell',
                price: 450000,
                location: 'Residential Area',
                bedrooms: 3,
                bathrooms: 2,
                area: 2000,
                description: 'Perfect family home in a quiet neighborhood.',
                main_image: 'images/property3.jpg',
                property_type: 'house'
            }
        ];
    }
}

// Initialize property manager
const propertyManager = new PropertyManager(); 
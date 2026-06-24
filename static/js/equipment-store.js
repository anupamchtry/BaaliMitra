// Equipment Store JavaScript - Complete Interactive Features

// Sample data for demonstration
const equipmentData = {
    1: {
        id: 1,
        name: "Steel Hand Plow",
        description: "Heavy-duty steel plow for small plots",
        category: "soil",
        buyPrice: 2500,
        rentPrice: 150,
        image: "images/equipment/hand-plow.jpg",
        details: {
            specifications: [
                "Material: High carbon steel",
                "Weight: 3.5 kg",
                "Handle: Wooden grip",
                "Blade width: 15 cm",
                "Warranty: 2 years"
            ],
            features: [
                "Rust resistant coating",
                "Ergonomic handle design",
                "Sharp cutting edge",
                "Suitable for all soil types"
            ],
            usage: "Ideal for breaking soil, making furrows, and preparing seedbeds in small to medium farms."
        },
        availability: "both"
    },
    2: {
        id: 2,
        name: "Electric Water Pump",
        description: "1 HP submersible pump for irrigation",
        category: "irrigation",
        buyPrice: 8500,
        rentPrice: 300,
        image: "images/equipment/water-pump.jpg",
        details: {
            specifications: [
                "Power: 1 HP (750W)",
                "Flow rate: 2000 L/hr",
                "Head: 25 meters",
                "Inlet/Outlet: 1 inch",
                "Cable length: 10 meters"
            ],
            features: [
                "Energy efficient motor",
                "Overload protection",
                "Corrosion resistant body",
                "Easy installation"
            ],
            usage: "Perfect for irrigation, water transfer, and drainage applications in farms and gardens."
        },
        availability: "both"
    },
    3: {
        id: 3,
        name: "Manual Seed Drill",
        description: "9-row manual seed drill for precise planting",
        category: "planting",
        buyPrice: 15000,
        rentPrice: 0,
        image: "images/equipment/seed-drill.jpg",
        details: {
            specifications: [
                "Rows: 9 rows",
                "Row spacing: 20 cm",
                "Seed hopper: 15 kg capacity",
                "Weight: 25 kg",
                "Material: MS steel frame"
            ],
            features: [
                "Adjustable seed rate",
                "Uniform seed placement",
                "Easy to operate",
                "Suitable for various seeds"
            ],
            usage: "Efficient for planting wheat, rice, maize, and other crops with precise spacing and depth."
        },
        availability: "buy"
    },
    4: {
        id: 4,
        name: "Steel Harvesting Sickle",
        description: "Sharp curved blade for efficient harvesting",
        category: "harvesting",
        buyPrice: 750,
        rentPrice: 0,
        image: "images/equipment/sickle.jpg",
        details: {
            specifications: [
                "Blade length: 30 cm",
                "Handle length: 15 cm",
                "Material: Carbon steel",
                "Weight: 0.8 kg",
                "Edge angle: 45 degrees"
            ],
            features: [
                "Sharp cutting edge",
                "Comfortable grip handle",
                "Lightweight design",
                "Long lasting sharpness"
            ],
            usage: "Traditional tool for harvesting grains, cutting grass, and general farm maintenance work."
        },
        availability: "buy"
    }
};

const machineryData = {
    101: {
        id: 101,
        name: "Mahindra 575 DI",
        type: "tractor",
        brand: "mahindra",
        hp: 45,
        dailyRate: 1800,
        weeklyRate: 11000,
        location: "Varanasi",
        availability: "available",
        image: "images/machinery/tractor-mahindra.jpg",
        details: {
            specifications: [
                "Engine: 2730 CC, 4 Cylinder",
                "Power: 45 HP",
                "Fuel Tank: 65 Liters",
                "Lifting Capacity: 1800 kg",
                "PTO Power: 38 HP",
                "Gears: 8 Forward + 2 Reverse"
            ],
            features: [
                "Power steering",
                "Oil immersed brakes",
                "Dual clutch",
                "Advanced hydraulics",
                "Comfortable seating"
            ],
            applications: [
                "Plowing and tilling",
                "Sowing and planting",
                "Harvesting operations",
                "Transportation",
                "PTO operations"
            ]
        },
        securityDeposit: 15000
    },
    102: {
        id: 102,
        name: "John Deere W70",
        type: "harvester",
        brand: "john-deere",
        hp: 120,
        dailyRate: 4500,
        weeklyRate: 28000,
        location: "Lucknow",
        availability: "available",
        image: "images/machinery/harvester-john-deere.jpg",
        details: {
            specifications: [
                "Engine: 4045T, 4 Cylinder",
                "Power: 120 HP",
                "Cutting Width: 3.6 meters",
                "Grain Tank: 2300 liters",
                "Fuel Tank: 208 liters",
                "Ground Speed: 0-25 km/h"
            ],
            features: [
                "Hillside performance",
                "Efficient threshing",
                "Clean grain system",
                "Comfortable cab",
                "Easy maintenance"
            ],
            applications: [
                "Wheat harvesting",
                "Rice harvesting",
                "Barley harvesting",
                "Corn harvesting"
            ]
        },
        securityDeposit: 50000
    },
    103: {
        id: 103,
        name: "Swaraj Multi-Crop Thresher",
        type: "thresher",
        brand: "swaraj",
        hp: 25,
        dailyRate: 800,
        weeklyRate: 5000,
        location: "Kanpur",
        availability: "upcoming",
        image: "images/machinery/thresher-swaraj.jpg",
        details: {
            specifications: [
                "Engine: Single Cylinder Diesel",
                "Power: 25 HP",
                "Threshing Capacity: 15-20 quintals/hour",
                "Cleaning System: Multi-stage",
                "Dimensions: 4.5m x 2m x 2.5m"
            ],
            features: [
                "Multi-crop capability",
                "High efficiency",
                "Low grain damage",
                "Easy operation",
                "Portable design"
            ],
            applications: [
                "Wheat threshing",
                "Rice threshing",
                "Barley processing",
                "Pulse threshing"
            ]
        },
        securityDeposit: 8000
    }
};

// Global variables
let cartItems = [];
let currentProductId = null;
let currentMachineryId = null;

// DOM Elements
const searchInput = document.getElementById('searchInput');
const equipmentGrid = document.getElementById('equipment-grid');
const machineryGrid = document.getElementById('machinery-grid');
const cartCount = document.querySelector('.cart-count');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadCartFromStorage();
});

function initializeApp() {
    // Setup section toggles
    setupSectionToggle();
    
    // Setup category filters
    setupCategoryFilters();
    
    // Setup search functionality
    setupSearch();
    
    // Setup date inputs with current date
    setupDateInputs();
    
    // Setup form validations
    setupFormValidations();
}

function setupEventListeners() {
    // Store section toggle
    const optionBtns = document.querySelectorAll('.option-btn');
    optionBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetSection = btn.dataset.section;
            toggleStoreSection(targetSection);
        });
    });

    // Category cards click
    document.querySelectorAll('.category-card').forEach(card => {
        card.addEventListener('click', () => {
            const category = card.dataset.category;
            document.getElementById('equipment-category').value = category;
            filterProducts();
        });
    });

    // Wishlist buttons
    document.querySelectorAll('.wishlist-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleWishlist(btn);
        });
    });

    // Modal close events
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            closeModal(e.target.id);
        }
    });

    // Filter change events
    setupFilterEvents();
}

function setupSectionToggle() {
    const optionBtns = document.querySelectorAll('.option-btn');
    const sections = document.querySelectorAll('.store-section');
    
    optionBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetSection = btn.dataset.section;
            
            // Update buttons
            optionBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Update sections
            sections.forEach(section => {
                section.classList.remove('active');
                if (section.id === targetSection + '-section') {
                    section.classList.add('active');
                }
            });
        });
    });
}

function setupCategoryFilters() {
    // Equipment category filter
    const categoryFilter = document.getElementById('equipment-category');
    if (categoryFilter) {
        categoryFilter.addEventListener('change', filterProducts);
    }

    // Price range filter
    const priceFilter = document.getElementById('price-range');
    if (priceFilter) {
        priceFilter.addEventListener('change', filterProducts);
    }

    // Availability filter
    const availabilityFilter = document.getElementById('availability');
    if (availabilityFilter) {
        availabilityFilter.addEventListener('change', filterProducts);
    }
}

function setupSearch() {
    if (searchInput) {
        searchInput.addEventListener('input', debounce(performSearch, 300));
    }
}

function setupDateInputs() {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    const startDateInput = document.getElementById('startDate');
    const endDateInput = document.getElementById('endDate');
    
    if (startDateInput) {
        startDateInput.min = today.toISOString().split('T')[0];
        startDateInput.value = today.toISOString().split('T')[0];
    }
    
    if (endDateInput) {
        endDateInput.min = tomorrow.toISOString().split('T')[0];
        endDateInput.value = tomorrow.toISOString().split('T')[0];
    }
}

function setupFormValidations() {
    // Rental form date validation
    const startDate = document.getElementById('startDate');
    const endDate = document.getElementById('endDate');
    
    if (startDate && endDate) {
        startDate.addEventListener('change', calculateRentalCost);
        endDate.addEventListener('change', calculateRentalCost);
    }
}

function setupFilterEvents() {
    // Machinery filters
    const machineryFilters = [
        'machinery-type',
        'machinery-brand',
        'hp-range',
        'machinery-price',
        'machinery-availability',
        'machinery-location'
    ];
    
    machineryFilters.forEach(filterId => {
        const filter = document.getElementById(filterId);
        if (filter) {
            filter.addEventListener('change', filterMachinery);
        }
    });
}

// Product functions
function openDetailsModal(productId) {
    currentProductId = productId;
    const product = equipmentData[productId];
    
    if (!product) return;
    
    const modal = document.getElementById('detailModal');
    const title = document.getElementById('detailTitle');
    const body = document.getElementById('detailBody');
    
    title.textContent = product.name;
    
    body.innerHTML = `
        <div class="detail-content">
            <div class="detail-image">
                <img src="${product.image}" alt="${product.name}" style="width: 100%; max-width: 300px; border-radius: 12px;">
            </div>
            
            <div class="detail-info">
                <h3>Product Overview</h3>
                <p>${product.description}</p>
                
                <div class="price-info">
                    ${product.buyPrice ? `<div class="price-item"><strong>Buy Price:</strong> ₹${product.buyPrice.toLocaleString()}</div>` : ''}
                    ${product.rentPrice ? `<div class="price-item"><strong>Rent Price:</strong> ₹${product.rentPrice}/day</div>` : ''}
                </div>
                
                <h4>Specifications</h4>
                <ul class="spec-list">
                    ${product.details.specifications.map(spec => `<li>${spec}</li>`).join('')}
                </ul>
                
                <h4>Key Features</h4>
                <ul class="feature-list">
                    ${product.details.features.map(feature => `<li>${feature}</li>`).join('')}
                </ul>
                
                <h4>Usage</h4>
                <p>${product.details.usage}</p>
                
                <div class="detail-actions">
                    ${product.buyPrice ? `<button class="primary-btn" onclick="openBuyModal(${productId})">
                        <i class="fas fa-shopping-cart"></i> Buy Now
                    </button>` : ''}
                    ${product.rentPrice ? `<button class="primary-btn" onclick="openRentModal(${productId})">
                        <i class="fas fa-calendar"></i> Rent Now
                    </button>` : ''}
                </div>
            </div>
        </div>
    `;
    
    showModal('detailModal');
}

function openBuyModal(productId) {
    currentProductId = productId;
    const product = equipmentData[productId];
    
    if (!product) return;
    
    const summary = document.getElementById('buyProductSummary');
    summary.innerHTML = `
        <div class="product-summary">
            <img src="${product.image}" alt="${product.name}">
            <div class="product-summary-info">
                <h3>${product.name}</h3>
                <p>${product.description}</p>
                <div class="price">₹${product.buyPrice.toLocaleString()}</div>
            </div>
        </div>
    `;
    
    showModal('buyModal');
}

function openRentModal(productId) {
    currentProductId = productId;
    const product = equipmentData[productId];
    
    if (!product) return;
    
    const summary = document.getElementById('rentProductSummary');
    summary.innerHTML = `
        <div class="product-summary">
            <img src="${product.image}" alt="${product.name}">
            <div class="product-summary-info">
                <h3>${product.name}</h3>
                <p>${product.description}</p>
                <div class="price">₹${product.rentPrice}/day</div>
            </div>
        </div>
    `;
    
    // Update daily rate display
    document.getElementById('dailyRate').textContent = `₹${product.rentPrice}`;
    
    calculateRentalCost();
    showModal('rentModal');
}

function addToCart(productId) {
    const product = equipmentData[productId];
    if (!product) return;
    
    // Check if item already in cart
    const existingItem = cartItems.find(item => item.id === productId);
    if (existingItem) {
        showToast('Item already in cart!', 'warning');
        return;
    }
    
    cartItems.push({
        id: productId,
        name: product.name,
        price: product.buyPrice,
        image: product.image,
        quantity: 1
    });
    
    updateCartCount();
    saveCartToStorage();
    showToast('Added to cart!', 'success');
}

function removeFromCart(productId) {
    cartItems = cartItems.filter(item => item.id !== productId);
    updateCartCount();
    saveCartToStorage();
    updateCartDisplay();
    showToast('Removed from cart', 'info');
}

function updateCartCount() {
    if (cartCount) {
        cartCount.textContent = cartItems.length;
    }
}

function updateCartDisplay() {
    const cartItemsContainer = document.getElementById('cartItems');
    if (!cartItemsContainer) return;
    
    if (cartItems.length === 0) {
        cartItemsContainer.innerHTML = `
            <div class="empty-cart">
                <i class="fas fa-shopping-cart"></i>
                <p>Your cart is empty</p>
                <button class="primary-btn" onclick="closeModal('cartModal')">Continue Shopping</button>
            </div>
        `;
        return;
    }
    
    const totalAmount = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    
    cartItemsContainer.innerHTML = `
        ${cartItems.map(item => `
            <div class="cart-item">
                <img src="${item.image}" alt="${item.name}">
                <div class="cart-item-info">
                    <h4>${item.name}</h4>
                    <div class="cart-item-price">₹${item.price.toLocaleString()}</div>
                </div>
                <button class="remove-item" onclick="removeFromCart(${item.id})">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `).join('')}
        <div class="cart-total">
            <div class="total-row">
                <span>Total: ₹${totalAmount.toLocaleString()}</span>
            </div>
            <div class="cart-actions">
                <button class="primary-btn" onclick="proceedToCheckout()">
                    <i class="fas fa-credit-card"></i> Proceed to Checkout
                </button>
            </div>
        </div>
    `;
}

function openCart() {
    updateCartDisplay();
    showModal('cartModal');
}

function proceedToCheckout() {
    if (cartItems.length === 0) return;
    
    closeModal('cartModal');
    
    // For demo purposes, simulate checkout process
    showSuccessModal('Order Placed!', 'Your order has been placed successfully. We will contact you shortly for delivery details.');
    
    // Clear cart
    cartItems = [];
    updateCartCount();
    saveCartToStorage();
}

// Machinery functions
function openMachineryDetailsModal(machineryId) {
    currentMachineryId = machineryId;
    const machinery = machineryData[machineryId];
    
    if (!machinery) return;
    
    const modal = document.getElementById('detailModal');
    const title = document.getElementById('detailTitle');
    const body = document.getElementById('detailBody');
    
    title.textContent = machinery.name;
    
    body.innerHTML = `
        <div class="detail-content">
            <div class="detail-image">
                <img src="${machinery.image}" alt="${machinery.name}" style="width: 100%; max-width: 300px; border-radius: 12px;">
            </div>
            
            <div class="detail-info">
                <div class="machinery-overview">
                    <h3>Machinery Overview</h3>
                    <div class="overview-specs">
                        <div class="spec-item"><strong>Type:</strong> ${machinery.type}</div>
                        <div class="spec-item"><strong>Brand:</strong> ${machinery.brand}</div>
                        <div class="spec-item"><strong>Power:</strong> ${machinery.hp} HP</div>
                        <div class="spec-item"><strong>Location:</strong> ${machinery.location}</div>
                        <div class="spec-item"><strong>Availability:</strong> ${machinery.availability}</div>
                    </div>
                </div>
                
                <div class="rental-pricing">
                    <h4>Rental Rates</h4>
                    <div class="price-grid">
                        <div class="price-item">
                            <span class="rate">₹${machinery.dailyRate}</span>
                            <span class="period">per day</span>
                        </div>
                        <div class="price-item">
                            <span class="rate">₹${machinery.weeklyRate}</span>
                            <span class="period">per week</span>
                        </div>
                    </div>
                    <div class="deposit-info">
                        <strong>Security Deposit:</strong> ₹${machinery.securityDeposit.toLocaleString()}
                    </div>
                </div>
                
                <h4>Technical Specifications</h4>
                <ul class="spec-list">
                    ${machinery.details.specifications.map(spec => `<li>${spec}</li>`).join('')}
                </ul>
                
                <h4>Key Features</h4>
                <ul class="feature-list">
                    ${machinery.details.features.map(feature => `<li>${feature}</li>`).join('')}
                </ul>
                
                <h4>Applications</h4>
                <ul class="application-list">
                    ${machinery.details.applications.map(app => `<li>${app}</li>`).join('')}
                </ul>
                
                <div class="detail-actions">
                    ${machinery.availability === 'available' ? 
                        `<button class="primary-btn" onclick="openMachineryRentModal(${machineryId})">
                            <i class="fas fa-calendar-check"></i> Rent Now
                        </button>` : 
                        `<button class="primary-btn disabled">
                            <i class="fas fa-clock"></i> Available Soon
                        </button>`
                    }
                </div>
            </div>
        </div>
    `;
    
    showModal('detailModal');
}

function openMachineryRentModal(machineryId) {
    currentMachineryId = machineryId;
    const machinery = machineryData[machineryId];
    
    if (!machinery) return;
    
    const summary = document.getElementById('rentProductSummary');
    summary.innerHTML = `
        <div class="product-summary">
            <img src="${machinery.image}" alt="${machinery.name}">
            <div class="product-summary-info">
                <h3>${machinery.name}</h3>
                <p>${machinery.brand} - ${machinery.hp} HP</p>
                <div class="price">₹${machinery.dailyRate}/day</div>
            </div>
        </div>
    `;
    
    // Update daily rate and security deposit
    document.getElementById('dailyRate').textContent = `₹${machinery.dailyRate}`;
    document.getElementById('securityDeposit').textContent = `₹${machinery.securityDeposit.toLocaleString()}`;
    
    calculateRentalCost();
    showModal('rentModal');
}

// Utility functions
function calculateRentalCost() {
    const startDate = document.getElementById('startDate');
    const endDate = document.getElementById('endDate');
    const rentalDaysEl = document.getElementById('rentalDays');
    const totalAmountEl = document.getElementById('totalAmount');
    
    if (!startDate || !endDate || !startDate.value || !endDate.value) return;
    
    const start = new Date(startDate.value);
    const end = new Date(endDate.value);
    const timeDiff = end.getTime() - start.getTime();
    const daysDiff = Math.ceil(timeDiff / (1000 * 3600 * 24));
    
    if (daysDiff <= 0) {
        rentalDaysEl.textContent = '0';
        totalAmountEl.textContent = '₹0';
        return;
    }
    
    let dailyRate = 0;
    if (currentProductId && equipmentData[currentProductId]) {
        dailyRate = equipmentData[currentProductId].rentPrice;
    } else if (currentMachineryId && machineryData[currentMachineryId]) {
        dailyRate = machineryData[currentMachineryId].dailyRate;
    }
    
    const totalAmount = daysDiff * dailyRate;
    
    rentalDaysEl.textContent = daysDiff;
    totalAmountEl.textContent = `₹${totalAmount.toLocaleString()}`;
}

function filterProducts() {
    const categoryFilter = document.getElementById('equipment-category').value;
    const priceFilter = document.getElementById('price-range').value;
    const availabilityFilter = document.getElementById('availability').value;
    
    const productCards = document.querySelectorAll('.product-card');
    
    productCards.forEach(card => {
        let show = true;
        
        // Category filter
        if (categoryFilter && card.dataset.category !== categoryFilter) {
            show = false;
        }
        
        // Price filter
        if (priceFilter && show) {
            const price = parseInt(card.dataset.price);
            const [min, max] = priceFilter.split('-').map(p => p.replace('+', ''));
            
            if (max) {
                if (price < parseInt(min) || price > parseInt(max)) {
                    show = false;
                }
            } else {
                if (price < parseInt(min)) {
                    show = false;
                }
            }
        }
        
        // Availability filter
        if (availabilityFilter && show) {
            const productId = card.dataset.productId;
            const product = equipmentData[productId];
            
            if (product && product.availability !== availabilityFilter && availabilityFilter !== 'both') {
                if (availabilityFilter === 'buy' && !product.buyPrice) show = false;
                if (availabilityFilter === 'rent' && !product.rentPrice) show = false;
            }
        }
        
        card.style.display = show ? 'block' : 'none';
    });
}

function filterMachinery() {
    const typeFilter = document.getElementById('machinery-type').value;
    const brandFilter = document.getElementById('machinery-brand').value;
    const hpFilter = document.getElementById('hp-range').value;
    const priceFilter = document.getElementById('machinery-price').value;
    const availabilityFilter = document.getElementById('machinery-availability').value;
    const locationFilter = document.getElementById('machinery-location').value;
    
    const machineryCards = document.querySelectorAll('.machinery-card');
    
    machineryCards.forEach(card => {
        let show = true;
        
        // Type filter
        if (typeFilter && card.dataset.type !== typeFilter) {
            show = false;
        }
        
        // Brand filter
        if (brandFilter && show && card.dataset.brand !== brandFilter) {
            show = false;
        }
        
        // HP filter
        if (hpFilter && show) {
            const hp = parseInt(card.dataset.hp);
            const [min, max] = hpFilter.split('-').map(p => p.replace('+', ''));
            
            if (max) {
                if (hp < parseInt(min) || hp > parseInt(max)) {
                    show = false;
                }
            } else {
                if (hp < parseInt(min)) {
                    show = false;
                }
            }
        }
        
        // Price filter
        if (priceFilter && show) {
            const price = parseInt(card.dataset.price);
            const [min, max] = priceFilter.split('-').map(p => p.replace('+', ''));
            
            if (max) {
                if (price < parseInt(min) || price > parseInt(max)) {
                    show = false;
                }
            } else {
                if (price < parseInt(min)) {
                    show = false;
                }
            }
        }
        
        // Availability filter
        if (availabilityFilter && show) {
            const machineryId = card.dataset.machineryId;
            const machinery = machineryData[machineryId];
            
            if (machinery && availabilityFilter === 'available' && machinery.availability !== 'available') {
                show = false;
            }
            if (machinery && availabilityFilter === 'upcoming' && machinery.availability !== 'upcoming') {
                show = false;
            }
        }
        
        card.style.display = show ? 'block' : 'none';
    });
}

function performSearch() {
    const query = searchInput.value.toLowerCase().trim();
    if (!query) {
        // Show all items if search is empty
        document.querySelectorAll('.product-card, .machinery-card').forEach(card => {
            card.style.display = 'block';
        });
        return;
    }
    
    // Search in products
    document.querySelectorAll('.product-card').forEach(card => {
        const title = card.querySelector('h3').textContent.toLowerCase();
        const description = card.querySelector('.product-description').textContent.toLowerCase();
        
        if (title.includes(query) || description.includes(query)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
    
    // Search in machinery
    document.querySelectorAll('.machinery-card').forEach(card => {
        const title = card.querySelector('h3').textContent.toLowerCase();
        const specs = Array.from(card.querySelectorAll('.spec')).map(spec => spec.textContent.toLowerCase()).join(' ');
        
        if (title.includes(query) || specs.includes(query)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function toggleWishlist(btn) {
    const icon = btn.querySelector('i');
    if (icon.classList.contains('far')) {
        icon.classList.remove('far');
        icon.classList.add('fas');
        btn.style.color = '#FF8C00';
        showToast('Added to wishlist!', 'success');
    } else {
        icon.classList.remove('fas');
        icon.classList.add('far');
        btn.style.color = '';
        showToast('Removed from wishlist', 'info');
    }
}

// Modal functions
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('show');
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('show');
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

function showSuccessModal(title, message, orderDetails = '') {
    document.getElementById('successTitle').textContent = title;
    document.getElementById('successMessage').textContent = message;
    document.getElementById('orderDetails').innerHTML = orderDetails;
    showModal('successModal');
}

// Form submission handlers
document.addEventListener('submit', function(e) {
    if (e.target.classList.contains('checkout-form')) {
        e.preventDefault();
        handlePurchaseSubmit(e.target);
    } else if (e.target.classList.contains('rental-form')) {
        e.preventDefault();
        handleRentalSubmit(e.target);
    }
});

function handlePurchaseSubmit(form) {
    const formData = new FormData(form);
    const product = equipmentData[currentProductId];
    
    // Simulate processing
    closeModal('buyModal');
    
    const orderDetails = `
        <div class="order-summary">
            <h4>Order Summary</h4>
            <div class="order-item">
                <strong>${product.name}</strong><br>
                Price: ₹${product.buyPrice.toLocaleString()}<br>
                Delivery to: ${formData.get('district')}
            </div>
        </div>
    `;
    
    showSuccessModal('Purchase Confirmed!', 'Your order has been placed successfully. We will contact you shortly for delivery arrangements.', orderDetails);
}

function handleRentalSubmit(form) {
    const formData = new FormData(form);
    const isEquipment = currentProductId !== null;
    const item = isEquipment ? equipmentData[currentProductId] : machineryData[currentMachineryId];
    
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const totalAmount = document.getElementById('totalAmount').textContent;
    
    // Simulate processing
    closeModal('rentModal');
    
    const orderDetails = `
        <div class="order-summary">
            <h4>Rental Summary</h4>
            <div class="order-item">
                <strong>${item.name}</strong><br>
                Rental Period: ${startDate} to ${endDate}<br>
                Total Amount: ${totalAmount}<br>
                ${!isEquipment ? `Security Deposit: ₹${item.securityDeposit.toLocaleString()}` : ''}
            </div>
        </div>
    `;
    
    showSuccessModal('Rental Confirmed!', 'Your rental booking has been confirmed. We will contact you shortly to arrange pickup/delivery.', orderDetails);
}

// Storage functions
function saveCartToStorage() {
    localStorage.setItem('baalimitra_cart', JSON.stringify(cartItems));
}

function loadCartFromStorage() {
    const saved = localStorage.getItem('baalimitra_cart');
    if (saved) {
        cartItems = JSON.parse(saved);
        updateCartCount();
    }
}

// Toast notification system
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <i class="fas fa-${getToastIcon(type)}"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Show toast
    setTimeout(() => toast.classList.add('show'), 100);
    
    // Hide toast
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function getToastIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// Utility function for debouncing
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Global functions for onclick handlers
window.openDetailsModal = openDetailsModal;
window.openBuyModal = openBuyModal;
window.openRentModal = openRentModal;
window.addToCart = addToCart;
window.removeFromCart = removeFromCart;
window.openCart = openCart;
window.proceedToCheckout = proceedToCheckout;
window.openMachineryDetailsModal = openMachineryDetailsModal;
window.openMachineryRentModal = openMachineryRentModal;
window.closeModal = closeModal;
window.showModal = showModal;
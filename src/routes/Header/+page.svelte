    <script lang="ts">
        import { onMount } from 'svelte';
        import { writable } from 'svelte/store'; // Make sure to import writable

        let isSideNavOpen = false;
        let isClosing = false;
        let username = writable('');
        let email = writable('');

        // Function to fetch user details from the backend
    async function getUserDetails() {
        try {
            const response = await fetch('http://localhost:5000/api/events', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('authToken')}` // Include token if needed
                }
            });
            
            if (response.ok) {
                const userData = await response.json();
                username.set(userData.username);  // Set the fetched username
                email.set(userData.email);  // Set the fetched email
            } else {
                // Handle error if user data is not found
                username.set('Guest');
                email.set('Not available');
            }
        } catch (error) {
            console.error('Error fetching user details:', error);
            username.set('Guest');
            email.set('Not available');
        }
    }

    function toggleSideNav() {
        if (isSideNavOpen) {
            isClosing = true;
            setTimeout(() => {
                isSideNavOpen = false;
                isClosing = false;
            }, 300); // Match the duration of the slide animation
        } else {
            isSideNavOpen = true;
        }
    }

    // Close nav when clicking outside
    function handleOutsideClick(event: MouseEvent) {
        const sideNav = document.getElementById('side-nav');
        const easynergyLogo = document.getElementById('easynergy-logo');
        
        if (isSideNavOpen && 
            sideNav && 
            easynergyLogo && 
            !sideNav.contains(event.target as Node) && 
            !easynergyLogo.contains(event.target as Node)
        ) {
            toggleSideNav();
        }
    }

    onMount(() => {
        getUserDetails(); // Get the user details when the component mounts
        document.addEventListener('click', handleOutsideClick);
        
        return () => {
            document.removeEventListener('click', handleOutsideClick);
        };
    });

    // Define the logout function
    function logout() {
        // Clear session or token
        localStorage.removeItem('authToken'); // Example: remove auth token
        sessionStorage.clear(); // Example: clear session storage

        // Redirect to login or logout endpoint
        window.location.href = '/'; // Replace with your backend logout route
    }
    </script>

    <style>
        .header-container {
            position: fixed;
            top: 0  ;
            left: 0;
            right: 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
            z-index: 900; /* Reduced z-index to be behind the side nav */
        }

        .right-logos {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .side-nav {
            position: fixed;
            top: 0;
            left: -300px;
            width: 300px;
            height: 100vh;
            background-color: #400000;
            transition: left 0.3s ease-in-out;
            z-index: 1000; /* Ensure side nav is above other elements */
        }

        .side-nav.open {
            left: 0;
        }

        .side-nav.closing {
            left: -300px;
        }

        .background-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url('/right_half_log.png');
            background-size: cover;
            background-position: center;
            opacity: 0.2;
            z-index: -1;
        }

        .easynergy-logo {
            width: 100px;
            cursor: pointer;
        }

        .user-info {
        margin-bottom: 20px;
        color: #fff;
    }

    .user-info p {
        margin: 0;
    }
    </style>

    <!-- Header Container -->
    <div class="header-container">
        <!-- EASYnergy Logo trigger -->
        <button
            id="easynergy-logo"
            aria-label="Toggle Side Navigation"
            on:click={toggleSideNav}
            on:keydown={(event) => event.key === 'Enter' && toggleSideNav()}
            style="background: none; border: none; padding: 0; cursor: pointer;"
        >
            <img src="/EASYnergy.png" alt="EASYnergy Logo" class="easynergy-logo"/>
        </button>

        <!-- Right Side Logos -->
        <div class="right-logos">
            <img src="/ccs_logo.png" alt="CCS Logo" class="w-20 h-auto"/>
            <img src="/gc_new_logo_2018.png" alt="GC Logo" class="w-20 h-auto"/>
        </div>
    </div>

    <!-- Side Navigation -->
    <div 
        id="side-nav"
        class="side-nav {isSideNavOpen ? 'open' : ''} {isClosing ? 'closing' : ''}"
    >
        <div class="background-overlay"></div>
        
        <div class="flex flex-col h-full p-6 text-white relative z-10">
            <!-- Navigation Title/Logo -->
    <!-- <div class="mb-5 text-left mt-0 pt-0">
        <img src="/EASYnergy.png" alt="EASYnergy" class="w-40 mb-4 mt-0 pt-0 mx-0"/>
    </div> -->



            <!-- Navigation Links -->
            <nav class="space-y-4 mt-[70px]">

                <h2 class="text-2xl mb-[40px] font-bold">Menu</h2>
                <a 
                    href="/Eventmain" 
                    class="block py-3 px-4 hover:bg-white hover:bg-opacity-20 rounded-md transition-colors">
                    <i class="fas fa-calendar mr-3"></i>My Events
                </a>

                <a 
                    href="/Reports" 
                    class="block py-3 px-4 hover:bg-white hover:bg-opacity-20 rounded-md transition-colors">
                    <i class="fas fa-chart-bar mr-3"></i>Reports
                </a>
            </nav>

            <div class="mt-auto">
                <button 
                    on:click={logout} 
                    class="block py-3 px-4 text-center bg-white bg-opacity-20 hover:bg-opacity-30 rounded-md transition-colors w-full">
                    <i class="fas fa-sign-out-alt mr-3"></i>Logout
                </button>
            </div>
            
            
        </div>
    </div>

    <head>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
    </head>
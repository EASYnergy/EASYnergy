
<script lang="ts">
    // Add any necessary script here for the header functionality if needed
</script>

<style>
    .header {
        display: flex;
        justify-content: space-evenly; /* Equal spacing between the options */
        align-items: center;
        padding: 20px 0;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 100;
        background-color: rgba(255, 255, 255, 0); /* Transparent background */
        box-shadow: none; /* Remove any background shadow */
    }

    .header-item {
        font-size: 1.2rem;
        color: #400000;
        font-weight: 600; /* White color for the text */
        text-decoration: none;
        padding: 10px;
        transition: color 0.3s ease;
    }

    .header-item:hover {
        color: #ff7f50; /* Change color on hover */
    }

    /* To make the page content appear below the header */
    .content {
        margin-top: 60px; /* Adjust based on the header's height */
    }
</style>

<!-- Header Component -->
<div class="header">
    <a href="/Eventmain" class="header-item">My Events</a>
    <a href="/Eventmain" class="header-item">Profile</a>
    <a href="/Eventmain" class="header-item">Reports</a>
    <a href="/Eventmain" class="header-item">Attendance</a>
    
</div>

<!-- Main Content -->
<div class="content">
    <!-- Add the content of the page below here -->
</div>

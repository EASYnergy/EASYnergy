<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import QRCode from 'qrcode'; // Importing the QRCode library
    import Header from '../Header/+page.svelte'; // Import Header component

    let userName: string = "John Doe"; // Example user name
    let searchQuery: string = ""; // Bind to the search input
    let createEventFormVisible = false; // Controls the visibility of the create event form

    // Sample event data
    let events = [
        { id: 1, name: "Tech Conference", date: "2024-12-15", location: "GCCCS Hall", description: "A conference on the latest in technology." },
        { id: 2, name: "Coding Workshop", date: "2024-12-18", location: "Room 101", description: "A hands-on workshop on full-stack development." },
        { id: 3, name: "Networking Event", date: "2024-12-20", location: "Online", description: "A virtual networking event for students and professionals." }
    ];

    // Computed property to filter events based on search query
    $: filteredEvents = events.filter(event => 
        event.name.toLowerCase().includes(searchQuery.toLowerCase())
    );

    // Simulate fetching events from a database
    const fetchEvents = async () => {
        console.log("Fetching events...");
        // Simulate a database call or API fetch
        // events = await fetch('/api/events');
    };

    // Event functions
    const viewEventDetails = (eventId: number) => {
        // Navigate to the EventPage with the specific event ID
        goto("/Eventpage");
    };

    const deleteEvent = (eventId: number) => {
        console.log(`Deleting event ID: ${eventId}`);
        // Implement delete logic here
    };

    onMount(() => {
        fetchEvents();
    });

    // Create Event Form
    let eventForm = {
        title: "",
        description: "",
        startTime: "",
        endTime: "",
    };

    let qrCodeData = ""; // Stores the generated QR code data
    let qrCodeImage = ""; // Stores the QR code image as a data URL

    const createEvent = () => {
        if (eventForm.title && eventForm.description && eventForm.startTime && eventForm.endTime) {
            qrCodeData = `Event: ${eventForm.title}\nDescription: ${eventForm.description}\nStart Time: ${eventForm.startTime}\nEnd Time: ${eventForm.endTime}`;

            QRCode.toDataURL(qrCodeData)
                .then(url => {
                    qrCodeImage = url;
                    // Optionally, you can save the event and show a success message
                })
                .catch(err => {
                    console.error("Error generating QR code", err);
                });
        } else {
            alert("Please fill in all the fields.");
        }
    };

    const cancelEventCreation = () => {
        // Reset form and hide modal
        eventForm = { title: "", description: "", startTime: "", endTime: "" };
        createEventFormVisible = false;
    };
</script>

<Header /> <!-- Render the Header component -->

<style>
    /* Modal background */
    .modal {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }

    /* Modal content */
    .modal-content {
        background-color: white;
        padding: 30px;
        border-radius: 8px;
        max-width: 500px;
        width: 100%;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* Close button style */
    .modal-close {
        position: absolute;
        top: 10px;
        right: 10px;
        background-color: transparent;
        border: none;
        font-size: 24px;
        font-weight: bold;
        cursor: pointer;
    }
</style>

<!-- Main Page Content -->
<div class="bg-transparent p-4 mt-6">
    <!-- Search Bar and Create Event Button -->
    <div class="flex flex-col sm:flex-row items-center mb-6 mt-[100px]">
        <!-- Search Bar -->
        <input
            type="text"
            placeholder="Search events..."
            class="w-full sm:w-2/3 md:w-3/4 px-4 py-2 bg-gray-100 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-500"
            bind:value={searchQuery}
        />
        
        <div class="pl-0 sm:pl-8 mt-4 sm:mt-0">
            <!-- Create Event Button -->
            <button 
                class="bg-orange-500 text-white py-2 px-6 rounded-md hover:bg-orange-600 transition-all"
                on:click={() => createEventFormVisible = true}
            >
                Create Event
            </button>
        </div>
    </div>

    <!-- Event List -->
    <div class="w-full">
        <table class="w-full table-auto">
            <thead>
                <tr>
                    <th class="bg-white bg-opacity-30 text-black py-2 px-4 text-left">Event Name</th>
                    <th class="bg-white bg-opacity-30 text-black py-2 px-4 text-left">Description</th>
                    <th class="bg-white bg-opacity-30 text-black py-2 px-4 text-left">Date</th>
                    <th class="bg-white bg-opacity-30 text-black py-2 px-4 text-left">Location</th>
                    <th class="bg-white bg-opacity-30 text-black py-2 px-4 text-left">View</th>
                    <th class="bg-white bg-opacity-30 text-black py-2 px-4 text-left">Delete</th>
                </tr>
            </thead>
            <tbody>
               {#each filteredEvents as event}
                    <tr class="hover:bg-gray-100">
                        <td class="py-2 px-4">{event.name}</td>
                        <td class="py-2 px-4">{event.description}</td>
                        <td class="py-2 px-4">{event.date}</td>
                        <td class="py-2 px-4">{event.location}</td>
                        <td class="py-2 px-4">
                            <button class="bg-blue-500 text-white py-1 px-4 rounded-md hover:bg-blue-600" on:click={() => viewEventDetails(event.id)}>View</button>
                        </td>
                        <td class="py-2 px-4">
                            <button class="bg-red-500 text-white py-1 px-4 rounded-md hover:bg-red-600" on:click={() => deleteEvent(event.id)}>Delete</button>
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
</div>

<!-- Modal for Create Event Form -->
{#if createEventFormVisible}
    <div class="modal">
        <div class="modal-content">
            <!-- Close Button -->
            <button class="modal-close" on:click={() => cancelEventCreation()}>×</button>
            
            <h2 class="text-2xl font-bold mb-4">Create New Event</h2>

            <!-- Event Form -->
            <form class="space-y-4">
                <div>
                    <label for="event-title" class="block text-gray-700">Event Title</label>
                    <input 
                        type="text" 
                        id="event-title"
                        bind:value={eventForm.title} 
                        class="w-full px-4 py-2 border border-gray-300 rounded-md"
                        placeholder="Enter event title"
                    />
                </div>
            
                <div>
                    <label for="event-description" class="block text-gray-700">Description</label>
                    <textarea 
                        id="event-description"
                        bind:value={eventForm.description} 
                        class="w-full px-4 py-2 border border-gray-300 rounded-md"
                        placeholder="Enter event description"
                    ></textarea>
                </div>
            
                <div>
                    <label for="start-time" class="block text-gray-700">Start Time</label>
                    <input 
                        type="datetime-local"
                        id="start-time"
                        bind:value={eventForm.startTime}
                        class="w-full px-4 py-2 border border-gray-300 rounded-md"
                    />
                </div>
            
                <div>
                    <label for="end-time" class="block text-gray-700">End Time</label>
                    <input 
                        type="datetime-local"
                        id="end-time"
                        bind:value={eventForm.endTime}
                        class="w-full px-4 py-2 border border-gray-300 rounded-md"
                    />
                </div>

                <!-- QR Code Preview -->
                {#if qrCodeImage}
                    <div class="text-xl font-semibold mb-2">Generated QR Code</div>
                    <img src={qrCodeImage} alt="QR Code" class="w-32 h-32" />
                {/if}

                <div class="flex justify-between">
                    <!-- Cancel Button -->
                    <button 
                        type="button" 
                        on:click={cancelEventCreation}
                        class="bg-gray-500 text-white py-2 px-6 rounded-md hover:bg-gray-600"
                    >
                        Cancel
                    </button>

                    <!-- Submit Button -->
                    <button 
                        type="button" 
                        on:click={createEvent}
                        class="bg-green-500 text-white py-2 px-6 rounded-md hover:bg-green-600"
                    >
                        Create Event
                    </button>
                </div>
            </form>
        </div>
    </div>
{/if}

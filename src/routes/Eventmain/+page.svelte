<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import QRCode from 'qrcode';
    import Header from '../Header/+page.svelte';

    let userName: string = "John Doe"; // Example user name
    let searchQuery: string = ""; // Bind to the search input
    let createEventFormVisible = false; // Controls the visibility of the create event form
    let editEventFormVisible = false; // Controls the visibility of the edit event form

    // Define the type for an Event
    type Event = {
        id: number;
        name: string;
        date: string;
        location: string;
        description: string;
    };

    let events: Event[] = [];

    // Computed property to filter events based on search query
    $: filteredEvents = events.filter(event => 
        event.name.toLowerCase().includes(searchQuery.toLowerCase())
    );

    // Fetch events from the database
    const fetchEvents = async () => {
        try {
            const response = await fetch('http://localhost/EASYnergy/events.php');
            if (!response.ok) throw new Error('Failed to fetch events');
            const data = await response.json();

            // Map the fields to match the frontend structure
            events = data.map((event: any) => ({
                id: event.event_id || 0,
                name: event.event_name || "Untitled Event",
                description: event.event_description || "No Description",
                location: event.location || "Unknown Location",
                date: event.event_date || "N/A",
            }));
        } catch (error) {
            console.error('Error fetching events:', error);
            alert('Error fetching events. Please try again later.');
        }
    };

    const viewEventDetails = (eventId: number) => {
        goto(`/Eventpage?id=${eventId}`);
    };

    const deleteEvent = async (eventId: number) => {
        try {
            const response = await fetch(`http://localhost/EASYnergy/events.php?event_id=${eventId}`, {
                method: 'DELETE',
            });

            if (response.ok) {
                alert('Event deleted successfully!');
                fetchEvents();
            } else {
                const errorResponse = await response.json();
                throw new Error(errorResponse.error || 'Failed to delete event');
            }
        } catch (error) {
            console.error(error);
            alert('Error deleting event. Please try again later.');
        }
    };

            let eventForm: { 
            id: number | null; // id can be number or null
            title: string; 
            description: string; 
            location: string; 
            startTime: string; 
            endTime: string; 
        } = {
            id: null, // Initialize with null
            title: "", 
            description: "", 
            location: "", 
            startTime: "", 
            endTime: ""
        };
    const createEvent = async () => {
        if (eventForm.title && eventForm.description && eventForm.startTime && eventForm.endTime && eventForm.location) {
            try {
                const qrCodeData = `Event: ${eventForm.title}\nDescription: ${eventForm.description}\nStart Time: ${eventForm.startTime}\nEnd Time: ${eventForm.endTime}\nLocation: ${eventForm.location}`;
                const qrCodeURL = await QRCode.toDataURL(qrCodeData);

                const newEvent = {
                    user_id: 1,
                    event_name: eventForm.title,
                    event_description: eventForm.description,
                    location: eventForm.location,
                    event_date: eventForm.startTime.split('T')[0],
                    start_time: eventForm.startTime,
                    end_time: eventForm.endTime,
                    qr_code: qrCodeURL,
                };

                const response = await fetch('http://localhost/EASYnergy/events.php', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(newEvent),
                });

                if (response.ok) {
                    alert('Event created successfully!');
                    fetchEvents();
                    cancelEventCreation();
                } else {
                    const errorResponse = await response.json();
                    throw new Error(errorResponse.error || 'Failed to create event');
                }
            } catch (error) {
                console.error(error);
                alert('Error creating event. Please try again later.');
            }
        } else {
            alert('Please fill in all fields.');
        }
    };

    const editEvent = (event: Event) => {
    eventForm = {
        id: event.id,  // Assign the event id here
        title: event.name,
        description: event.description,
        startTime: event.date + 'T12:00', // Adjust time as needed
        endTime: event.date + 'T14:00', // Adjust time as needed
        location: event.location
    };
    editEventFormVisible = true;
};

const updateEvent = async () => {
    if (eventForm.title && eventForm.description && eventForm.startTime && eventForm.endTime && eventForm.location) {
        try {
            // Generate QR Code for the updated event data
            const qrCodeData = `Event: ${eventForm.title}\nDescription: ${eventForm.description}\nStart Time: ${eventForm.startTime}\nEnd Time: ${eventForm.endTime}\nLocation: ${eventForm.location}`;
            const qrCodeURL = await QRCode.toDataURL(qrCodeData);

            // Prepare the updated event data
            const updatedEvent = {
                event_id: eventForm.id, // The ID of the event being updated
                user_id: 1, // Example user_id; adjust as needed
                event_name: eventForm.title,
                event_description: eventForm.description,
                location: eventForm.location,
                event_date: eventForm.startTime.split('T')[0],
                start_time: eventForm.startTime,
                end_time: eventForm.endTime,
                qr_code: qrCodeURL,
            };

            // Send the updated data to the server
            const response = await fetch(`http://localhost/EASYnergy/events.php?event_id=${eventForm.id}`, {
                method: 'PUT', // HTTP PUT method for updating
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(updatedEvent),
            });

            if (response.ok) {
                alert('Event updated successfully!');
                fetchEvents(); // Refresh events
                cancelEventEdit(); // Reset the form and close the modal
            } else {
                const errorResponse = await response.json();
                throw new Error(errorResponse.error || 'Failed to update event');
            }
        } catch (error) {
            console.error(error);
            alert('Error updating event. Please try again later.');
        }
    } else {
        alert('Please fill in all fields.');
    }
};

    const cancelEventCreation = () => {
    eventForm = { 
        id: null,  // Ensure the id is set to null for event creation
        title: "", 
        description: "", 
        startTime: "", 
        endTime: "", 
        location: "" 
    };
    createEventFormVisible = false;
    };

    const cancelEventEdit = () => {
    eventForm = { 
        id: null,  // Ensure id is reset to null
        title: "", 
        description: "", 
        startTime: "", 
        endTime: "", 
        location: "" 
    };
    editEventFormVisible = false;  // Hide the form after cancellation
    };


    onMount(() => {
        fetchEvents();
    });
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
                on:click={() => createEventFormVisible = true}>
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
                    <th class="bg-white bg-opacity-30 text-black py-2 px-4 text-left">Edit</th>
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
                        <td>
                            <button class="bg-yellow-500 text-white py-1 px-4 rounded-md hover:bg-yellow-600" 
                            on:click={() => editEvent(event)}>Edit</button>

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
            
            <h2 class="text-2xl font-bold mb-4">Event Creation Form</h2>

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
                    <label for="event-location" class="block text-gray-700">Location</label>
                    <input 
                        type="text"
                        id="event-location"
                        bind:value={eventForm.location} 
                        class="w-full px-4 py-2 border border-gray-300 rounded-md"
                        placeholder="Enter event location"
                    />
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
            
                <div class="flex justify-between">
                    <button 
                        type="button" 
                        on:click={cancelEventCreation}
                        class="bg-gray-500 text-white py-2 px-6 rounded-md hover:bg-gray-600">
                        Cancel
                    </button>
            
                    <button 
                        type="button" 
                        on:click={createEvent}
                        class="bg-green-500 text-white py-2 px-6 rounded-md hover:bg-green-600">
                        Create Event
                    </button>
                </div>
            </form>
        </div>
    </div>
{/if}

{#if editEventFormVisible}
    <div class="modal">
        <div class="modal-content">
            <!-- Close Button -->
            <button class="modal-close" on:click={() => cancelEventEdit()}>×</button>
            
            <h2 class="text-2xl font-bold mb-4">Edit Event</h2>

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
                    <label for="event-location" class="block text-gray-700">Location</label>
                    <input 
                        type="text"
                        id="event-location"
                        bind:value={eventForm.location} 
                        class="w-full px-4 py-2 border border-gray-300 rounded-md"
                        placeholder="Enter event location"
                    />
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
            
                <div class="flex justify-between">
                    <button 
                        type="button" 
                        on:click={cancelEventEdit}
                        class="bg-gray-500 text-white py-2 px-6 rounded-md hover:bg-gray-600">
                        Cancel
                    </button>
            
                    <button 
                        type="button" 
                        on:click={updateEvent}
                        class="bg-blue-500 text-white py-2 px-6 rounded-md hover:bg-blue-600">
                        Save Changes
                    </button>
                </div>
            </form>
        </div>
    </div>
{/if}

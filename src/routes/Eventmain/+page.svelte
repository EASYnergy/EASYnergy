<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import QRCode from 'qrcode';
    import Header from '../Header/+page.svelte';

    let qrModalVisible = false;
    let qrImageSrc = "";
    let qrEventName = "";
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
        speaker: string;
    };

    let events: Event[] = [];

    // Computed property to filter events based on search query
    $: filteredEvents = events.filter(event => 
        event.name.toLowerCase().includes(searchQuery.toLowerCase())
    );

    // Fetch events from the database
    const fetchEvents = async () => {
    try {
        const response = await fetch('http://localhost:5000/api/events');
        if (!response.ok) {
            const errorResponse = await response.json();
            throw new Error(errorResponse.error || `Failed to fetch events (Status: ${response.status})`);
        }
        const data = await response.json();
        events = data.map((event: any) => ({
            id: event.event_id || 0,
            name: event.event_name || "Untitled Event",
            description: event.event_description || "No Description",
            location: event.location || "Unknown Location",
            date: event.event_date || "N/A",
            speaker: event.speaker || "Unknown Speaker",
        }));
    } catch (error: unknown) {
        if (error instanceof Error) {
            console.error('Error fetching events:', error.message);
            alert(`Error fetching events: ${error.message}`);
        } else {
            console.error('An unknown error occurred:', error);
            alert('An unknown error occurred while fetching events.');
        }
    }
};



    const viewEventDetails = (eventId: number) => {
        goto(`/Eventpage?id=${eventId}`);
    };

    

    const deleteEvent = async (eventId: number) => {
    try {
        const response = await fetch(`http://localhost:5000/api/events/${eventId}`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            // Log the error response for debugging
            const errorDetails = await response.json();
            console.error('Server responded with:', errorDetails);
            throw new Error(`Failed to delete event (Status: ${response.status}): ${errorDetails.error || 'Unknown error'}`);
        }

        alert('Event deleted successfully!');
        fetchEvents(); // Refresh the list of events
    } catch (error) {
        // Comprehensive error handling
        if (error instanceof Error) {
            console.error('Error deleting event:', error.message);
            alert(`Error deleting event: ${error.message}`);
        } else {
            console.error('An unknown error occurred:', error);
            alert('An unknown error occurred while deleting the event.');
        }
    }
};



    let eventForm: { 
    id: number | null;
    title: string;
    description: string;
    location: string;
    speaker: string; // Added field
    startTime: string;
    endTime: string;
} = {
    id: null,
    title: "",
    description: "",
    location: "",
    speaker: "", // Initialize speaker
    startTime: "",
    endTime: ""
};

const validateEventForm = () => {
    if (!eventForm.title.trim()) return 'Title is required.';
    if (!eventForm.description.trim()) return 'Description is required.';
    if (!eventForm.location.trim()) return 'Location is required.';
    if (!eventForm.speaker.trim()) return 'Speaker is required.';
    if (!eventForm.startTime || !Date.parse(eventForm.startTime)) return 'Valid start time is required.';
    if (!eventForm.endTime || !Date.parse(eventForm.endTime)) return 'Valid end time is required.';
    return null; // No validation errors
};

const createEvent = async () => {
    const validationError = validateEventForm();
    if (validationError) {
        alert(validationError);
        return;
    }

    try {
        // Prepare event data without QR code
        const newEvent = {
            event_name: eventForm.title,
            event_description: eventForm.description,
            location: eventForm.location,
            speaker: eventForm.speaker || "",
            event_date: eventForm.startTime.split('T')[0],
            start_time: eventForm.startTime,
            end_time: eventForm.endTime,
        };

        // Send event data to the backend
        const response = await fetch('http://localhost:5000/api/events', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newEvent),
        });

        if (!response.ok) {
            const errorResponse = await response.json();
            throw new Error(errorResponse.error || `Failed to create event (Status: ${response.status})`);
        }

        const result = await response.json();
        alert(`Event created successfully! Event ID: ${result.event_id}`);
        fetchEvents();
        cancelEventCreation();
    } catch (error) {
        // Narrow the type of error
        if (error instanceof Error) {
            console.error(error);
            alert(`Error creating event: ${error.message}`);
        } else {
            console.error("An unknown error occurred:", error);
            alert("Error creating event: An unknown error occurred");
        }
    }
};



    const editEvent = (event: Event) => {
    eventForm = {
        id: event.id,  // Assign the event id here
        title: event.name,
        description: event.description,
        startTime: event.date + 'T12:00', // Adjust time as needed
        endTime: event.date + 'T14:00', // Adjust time as needed
        location: event.location,
        speaker: event.speaker
    };
    editEventFormVisible = true;
};

const updateEvent = async () => {
    if (eventForm.title && eventForm.description && eventForm.startTime && eventForm.endTime && eventForm.location && eventForm.speaker) {
        try {
            const qrCodeData = `Event: ${eventForm.title}\nDescription: ${eventForm.description}\nStart Time: ${eventForm.startTime}\nEnd Time: ${eventForm.endTime}\nLocation: ${eventForm.location}\nSpeaker: ${eventForm.speaker}`;
            const qrCodeURL = await QRCode.toDataURL(qrCodeData);

            const updatedEvent = {
                event_id: eventForm.id,
                user_id: 1,
                event_name: eventForm.title,
                event_description: eventForm.description,
                location: eventForm.location,
                speaker: eventForm.speaker, // Include speaker
                event_date: eventForm.startTime.split('T')[0],
                start_time: eventForm.startTime,
                end_time: eventForm.endTime,
                qr_code: qrCodeURL,
            };

            const response = await fetch(`http://localhost:5000/api/events`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updatedEvent),
        });


        if (!response.ok) {
         const errorText = await response.text();
            console.error('Error response from server:', errorText);
            throw new Error('Failed to update event. Check server logs for details.');
        }
            const result = await response.json();
            alert('Event updated successfully!');
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
        location: "",
        speaker: "" 
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
        location: "" ,
        speaker: ""
    };
    editEventFormVisible = false;  // Hide the form after cancellation
    };

    const generateQRCode = async (eventId: string): Promise<void> => {
    try {
        const response = await fetch(`http://localhost:5000/api/events/${eventId}/generate-qr`);
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || "Failed to generate QR code");
        }
        const data = await response.json();
        qrImageSrc = `data:image/png;base64,${data.qr_code}`;
        qrEventName = data.event_name;
        qrModalVisible = true;
    } catch (error) {
        if (error instanceof Error) {
            alert(`Error generating QR code: ${error.message}`);
        } else {
            alert("An unknown error occurred");
        }
    }
};


    const closeModal = () => {
        qrModalVisible = false;
        qrImageSrc = "";
        qrEventName = "";
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

        <!-- Create Event Button -->
        <div class="ml-auto mt-4 sm:mt-0 mr-2">
            <button 
                class="bg-orange-500 text-white py-2 px-6 rounded-md hover:bg-orange-600 transition-all"
                on:click={() => createEventFormVisible = true}>
                Create Event
            </button>
        </div>
    </div>

    <!-- Event List -->
    <div>
        <!-- Existing table code -->
        <div class="w-full">
            <table class="w-full table-auto">
                <thead>
                    <tr>
                        <th class="bg-white bg-opacity-30 text-black py-2 px-4 text-left">Event Name</th>
                        <th class="bg-white bg-opacity-30 text-black py-2 px-4 text-left">Description</th>
                        <th class="bg-white bg-opacity-30 text-black py-2 px-4 text-left">Date</th>
                        <th class="bg-white bg-opacity-30 text-black py-2 px-4 text-left">Location</th>
                        <th class="bg-white bg-opacity-30 text-black py-2 px-4 text-left">Speaker</th>
                        <th class="bg-white bg-opacity-30 text-black py-2 px-4 text-left">View</th>
                        <th class="bg-white bg-opacity-30 text-black py-2 px-4 text-left">Edit</th>
                        <th class="bg-white bg-opacity-30 text-black py-2 px-4 text-left">Delete</th>
                        <th class="bg-white bg-opacity-30 text-black py-2 px-4 text-left">Generate QR Code</th>
                    </tr>
                </thead>
                <tbody>
                    {#each filteredEvents as event, i}
                    <tr class={i % 2 === 0 ? 'bg-gray-100' : 'bg-white hover:bg-gray-200'}>
                        <td class="py-2 px-4">{event.name}</td>
                        <td class="py-2 px-4">{event.description}</td>
                        <td class="py-2 px-4">{event.date}</td>
                        <td class="py-2 px-4">{event.location}</td>
                        <td class="py-2 px-4">{event.speaker}</td>
                        <td class="py-2 px-4">
                            <button class="bg-blue-500 text-white py-1 px-4 rounded-md hover:bg-blue-600" on:click={() => viewEventDetails(event.id)}>View</button>
                        </td>
                        <td class="py-2 px-4">
                            <button class="bg-yellow-500 text-white py-1 px-4 rounded-md hover:bg-yellow-600" on:click={() => editEvent(event)}>Edit</button>
                        </td>
                        <td class="py-2 px-4">
                            <button class="bg-red-500 text-white py-1 px-4 rounded-md hover:bg-red-600" on:click={() => deleteEvent(event.id)}>Delete</button>
                        </td>
                        <td class="py-2 px-4">
                            <button 
                                class="bg-green-500 text-white py-1 px-4 rounded-md hover:bg-green-600" 
                                 on:click={() => generateQRCode(event.id.toString())}>
                                Generate QR Code
                            </button>
                        </td>
                    </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    
        <!-- Modal -->
        {#if qrModalVisible}
        <div class="fixed inset-0 bg-gray-800 bg-opacity-50 flex justify-center items-center z-50">
            <div class="bg-white p-6 rounded shadow-lg w-96">
                <h2 class="text-xl font-bold mb-4">{qrEventName} - QR Code</h2>
                <img src={qrImageSrc} alt="QR Code" class="w-full h-auto mb-4" />
                <button
                    class="bg-red-500 text-white py-2 px-4 rounded-md hover:bg-red-600 w-full"
                    on:click={closeModal}
                >
                    Close
                </button>
            </div>
        </div>
        {/if}
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
                        placeholder="Enter event title"/>
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
                        placeholder="Enter event location"/>
                </div>

                <div>
                    <label for="event-speaker" class="block text-gray-700">Speaker</label>
                    <input 
                        type="text"
                        id="event-speaker"
                        bind:value={eventForm.speaker} 
                        class="w-full px-4 py-2 border border-gray-300 rounded-md"
                        placeholder="Enter speaker name"/>
                </div>
            
                <div>
                    <label for="start-time" class="block text-gray-700">Start Time</label>
                    <input 
                        type="datetime-local"
                        id="start-time"
                        bind:value={eventForm.startTime}
                        class="w-full px-4 py-2 border border-gray-300 rounded-md"/>
                </div>
            
                <div>
                    <label for="end-time" class="block text-gray-700">End Time</label>
                    <input 
                        type="datetime-local"
                        id="end-time"
                        bind:value={eventForm.endTime}
                        class="w-full px-4 py-2 border border-gray-300 rounded-md"/>
                </div>

                <div class="flex justify-between mt-6">
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
                <!-- Event Title -->
                <div>
                    <label for="event-title" class="block text-gray-700">Event Title</label>
                    <input 
                        type="text" 
                        id="event-title"
                        bind:value={eventForm.title} 
                        class="w-full px-4 py-2 border border-gray-300 rounded-md"
                        placeholder="Enter event title"
                        required/>
                </div>

                <!-- Event Description -->
                <div>
                    <label for="event-description" class="block text-gray-700">Description</label>
                    <textarea 
                        id="event-description"
                        bind:value={eventForm.description} 
                        class="w-full px-4 py-2 border border-gray-300 rounded-md"
                        placeholder="Enter event description"
                        required
                    ></textarea>
                </div>

                <!-- Event Location -->
                <div>
                    <label for="event-location" class="block text-gray-700">Location</label>
                    <input 
                        type="text"
                        id="event-location"
                        bind:value={eventForm.location} 
                        class="w-full px-4 py-2 border border-gray-300 rounded-md"
                        placeholder="Enter event location"
                        required/>
                </div>

                <!-- Speaker -->
                <div>
                    <label for="event-speaker" class="block text-gray-700">Speaker</label>
                    <input 
                        type="text"
                        id="event-speaker"
                        bind:value={eventForm.speaker} 
                        class="w-full px-4 py-2 border border-gray-300 rounded-md"
                        placeholder="Enter speaker's name"
                        required/>
                </div>

                <!-- Start Time -->
                <div>
                    <label for="start-time" class="block text-gray-700">Start Time</label>
                    <input 
                        type="datetime-local"
                        id="start-time"
                        bind:value={eventForm.startTime}
                        class="w-full px-4 py-2 border border-gray-300 rounded-md"
                        required/>
                </div>

                <!-- End Time -->
                <div>
                    <label for="end-time" class="block text-gray-700">End Time</label>
                    <input 
                        type="datetime-local"
                        id="end-time"
                        bind:value={eventForm.endTime}
                        class="w-full px-4 py-2 border border-gray-300 rounded-md"
                        required/>
                </div>

                <!-- Form Actions -->
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


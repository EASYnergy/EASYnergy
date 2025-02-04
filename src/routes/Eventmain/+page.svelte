<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import QRCode from 'qrcode';
    import Header from '../Header/+page.svelte';

    let qrModalVisible = false;
    let qrImageSrc = "";
    let selectedFilter = "All Events";
    let qrEventName = "";
    let searchQuery: string = ""; // Search input binding
    let createEventFormVisible = false; // Controls the visibility of the create event form
    let editEventFormVisible = false; // Controls the visibility of the edit event form

    const filters = ["All Events", "Forums", "Seminar", "Workshop", "Training"];

    // Define the type for an Event
    type Event = {
        id: number;
        name: string;
        type: string;
        slot: number;
        date: string;
        location: string;
        description: string;
        speaker: string;
    };

    let events: Event[] = [];

    // Sort and filter events
    $: filteredEvents = events
        .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
        .filter(event => 
            event.name.toLowerCase().includes(searchQuery.toLowerCase())
        );

    const handleEventClick = (eventId: number, event?: MouseEvent | KeyboardEvent) => {
        if (event instanceof KeyboardEvent && event.key !== 'Enter' && event.key !== ' ') return;
        viewEventDetails(eventId);
    };

    const fetchEvents = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/events');
            if (!response.ok) {
                const errorResponse = await response.json();
                throw new Error(errorResponse.error || `Failed to fetch events (Status: ${response.status})`);
            }
            const data = await response.json();
            const today = new Date().toISOString().split('T')[0];
            events = data
                .filter((event: any) => new Date(event.event_date) >= new Date(today)) // Filter future or today events
                .map((event: any) => ({
                    id: event.event_id || 0,
                    name: event.event_name || "Untitled Event",
                    type: event.type || "Unknown",
                    slot: event.size || 0,
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
        const confirmDelete = confirm("Are you sure you want to delete this event? This action cannot be undone.");
        if (!confirmDelete) return;

        try {
            const response = await fetch(`http://localhost:5000/api/events/${eventId}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                const errorDetails = await response.json();
                throw new Error(`Failed to delete event (Status: ${response.status}): ${errorDetails.error || 'Unknown error'}`);
            }

            alert('Event deleted successfully!');
            fetchEvents();
        } catch (error) {
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
        type: string;
        slot: number | null;
        description: string;
        location: string;
        speaker: string;
        startTime: string;
        endTime: string;
    } = {
        id: null,
        title: "",
        type: "",
        slot: null,
        description: "",
        location: "",
        speaker: "",
        startTime: "",
        endTime: ""
    };

    const validateEventForm = () => {
        if (!eventForm.title.trim()) return 'Title is required.';
        if (!eventForm.type.trim()) return 'Type is required.';
        if (eventForm.slot === null || eventForm.slot <= 0) return 'Valid slot number is required.';
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
            const newEvent = {
                event_name: eventForm.title,
                type: eventForm.type,
                slot: eventForm.slot,
                event_description: eventForm.description,
                location: eventForm.location,
                speaker: eventForm.speaker,
                event_date: eventForm.startTime.split('T')[0],
                start_time: eventForm.startTime,
                end_time: eventForm.endTime,
            };

            const response = await fetch('http://localhost:5000/api/events', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newEvent),
            });

            if (!response.ok) {
                const errorResponse = await response.json();
                throw new Error(errorResponse.error || `Failed to create event (Status: ${response.status})`);
            }

            alert(`Event created successfully!`);
            fetchEvents();
            cancelEventCreation();
        } catch (error) {
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
        type: event.type,
        slot: event.slot,
        startTime: event.date + 'T12:00', // Adjust time as needed
        endTime: event.date + 'T14:00', // Adjust time as needed
        location: event.location,
        speaker: event.speaker
    };
    editEventFormVisible = true;
};



    const updateEvent = async () => {
        const validationError = validateEventForm();
        if (validationError) {
            alert(validationError);
            return;
        }

        try {
            const updatedEvent = {
                event_id: eventForm.id,
                event_name: eventForm.title,
                type: eventForm.type,
                slot: eventForm.slot,
                event_description: eventForm.description,
                location: eventForm.location,
                speaker: eventForm.speaker,
                event_date: eventForm.startTime.split('T')[0],
                start_time: eventForm.startTime,
                end_time: eventForm.endTime,
            };

            const response = await fetch('http://localhost:5000/api/events', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(updatedEvent),
            });

            if (!response.ok) {
                const errorResponse = await response.json();
                throw new Error(errorResponse.error || `Failed to update event (Status: ${response.status})`);
            }

            alert('Event updated successfully!');
            fetchEvents();
            cancelEventEdit();
        } catch (error) {
            if (error instanceof Error) {
                console.error(error);
                alert(`Error updating event: ${error.message}`);
            } else {
                console.error("An unknown error occurred:", error);
                alert("Error updating event: An unknown error occurred");
            }
        }
    };

    const cancelEventCreation = () => {
        eventForm = { 
            id: null,
            title: "",
            type: "",
            slot: null,
            description: "",
            location: "",
            speaker: "",
            startTime: "",
            endTime: ""
        };
        createEventFormVisible = false;
    };

    const cancelEventEdit = () => {
        eventForm = { 
            id: null,
            title: "",
            type: "",
            slot: null,
            description: "",
            location: "",
            speaker: "",
            startTime: "",
            endTime: ""
        };
        editEventFormVisible = false;
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
  @import url('https://fonts.googleapis.com/css2?family=Raleway:ital,wght@0,100..900;1,100..900&display=swap');


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

    /* Update event grid to 4 columns with responsive design */
    .event-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
    }

    /* Responsive adjustments */
    @media (max-width: 1200px) {
        .event-grid {
            grid-template-columns: repeat(3, 1fr);
        }
    }

    @media (max-width: 900px) {
        .event-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    @media (max-width: 600px) {
        .event-grid {
            grid-template-columns: 1fr;
        }
    }

    /* Event Box Styles */
    .event-box {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        padding: 16px;
        transition: transform 0.2s;
        display: flex;
        flex-direction: column;
        height: 100%;
    }

    .event-box:hover {
        transform: scale(1.05);
    }

    .event-title {
        font-size: 1.25rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 8px;
    }

    .event-details {
        color: #555;
        margin-bottom: 8px;
        flex-grow: 1;
    }

    .event-buttons {
        display: flex;
        justify-content: space-between;
        gap: 8px;
        margin-top: auto;
    }

    .event-action-buttons {
        display: flex;
        justify-content: flex-end;
        gap: 8px;
        margin-top: 12px;
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
            bind:value={searchQuery}/>

        <!-- Create Event Button -->
        <div class="ml-auto mt-4 sm:mt-0 mr-2">
            <button 
                class="bg-orange-500 text-white py-2 px-6 rounded-md hover:bg-orange-600 transition-all"
                on:click={() => createEventFormVisible = true}>
                Create Event
            </button>
        </div>
    </div>

    <!-- Event List in Grid Format -->
    <div class="event-grid grid gap-4 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
        {#each filteredEvents as event}
        <div class="bg-white rounded-lg shadow-md p-4 transition-transform duration-200 cursor-pointer flex flex-col h-full relative outline-none hover:scale-105" 
            role="button" 
            tabindex="0"
            on:click={() => handleEventClick(event.id)}
            on:keydown={(e) => handleEventClick(event.id, e)} >
                <!-- Event Title -->
                <div class="font-bold text-lg mb-2">{event.name}</div>

                <!-- Event Details -->
                <div class="flex-grow">
                    <p>{event.description}</p>
                    <p><strong>Type:</strong> {event.type}</p>
                    <p><strong>Date:</strong> {event.date}</p>
                    <p><strong>Location:</strong> {event.location}</p>
                    <p><strong>Speaker:</strong> {event.speaker}</p>
                </div>

                <!-- Action Buttons -->
                <div class="flex justify-between items-center mt-6 pt-4 border-t border-orange-500">
                    <!-- Edit Button -->
                    <button
                        on:click={(e) => { e.stopPropagation(); editEvent(event); }}
                        class="bg-orange-500 hover:bg-orange-600 text-white px-6 py-2 rounded-lg transition-colors duration-200 z-10">
                        Edit
                    </button>
                    
                    <!-- Delete Button -->
                    <button
                        on:click={(e) => { e.stopPropagation(); deleteEvent(event.id); }}
                        class="flex items-center justify-center w-10 h-10 bg-red-500 hover:bg-red-600 text-white rounded-full transition-colors duration-200"
                        aria-label="Delete event">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
            </div>
        {/each}
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

                <!-- New Type Field -->
                <div>
                    <label for="event-type" class="block text-gray-700">Type</label>
                    <select 
                        id="event-type" 
                        bind:value={eventForm.type} 
                        class="w-full px-4 py-2 border border-gray-300 rounded-md">
                        <option value="" disabled>Select type</option>
                        <option value="Forum">Forum</option>
                        <option value="Seminar">Seminar</option>
                        <option value="Workshop">Workshop</option>
                        <option value="Training">Training</option>
                    </select>
                </div>

                <!-- New Size Field -->
                <div>
                    <label for="event-size" class="block text-gray-700">Slots</label>
                    <input 
                        type="number" 
                        id="event-size" 
                        bind:value={eventForm.slot} 
                        class="w-full px-4 py-2 border border-gray-300 rounded-md"
                        placeholder="Enter number of slots"/>
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
                        class="bg-orange-500 text-white py-2 px-6 rounded-md hover:bg-orange-600">
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
                
                <!-- Event Type -->
                <div>
                    <label for="event-type" class="block text-gray-700">Type</label>
                    <select 
                        id="event-type" 
                        bind:value={eventForm.type} 
                        class="w-full px-4 py-2 border border-gray-300 rounded-md">
                        <option value="" disabled>Select type</option>
                        <option value="Forum">Forum</option>
                        <option value="Seminar">Seminar</option>
                        <option value="Workshop">Workshop</option>
                        <option value="Training">Training</option>
                    </select>
                </div>

                <!-- New Size Field -->
                <div>
                    <label for="event-size" class="block text-gray-700">Slots</label>
                    <input 
                        type="number" 
                        id="event-size" 
                        bind:value={eventForm.slot} 
                        class="w-full px-4 py-2 border border-gray-300 rounded-md"
                        placeholder="Enter number of slots"/>
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
                        class="bg-orange-500  text-white py-2 px-6 rounded-md hover:bg-red-600">
                        Save Changes
                    </button>
                </div>
            </form>
        </div>
    </div>
{/if}


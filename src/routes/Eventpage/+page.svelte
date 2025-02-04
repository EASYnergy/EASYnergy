<script lang="ts">
    import { page } from '$app/stores'; // Access route parameters
    import { goto } from '$app/navigation'; // For navigation
    import { onMount } from 'svelte';
    import jsQR from 'jsqr'; // Include this library in your project for QR code scanning


    let eventId: number;
    let event: any = null;
    let registeredStudents: any[] = [];
    let attendanceRecords: any[] = [];
    let loading = true;
    let error: string | null = null; // Explicitly typed as string or null
    let showModal = false;
    let videoStream: MediaStream | null = null;
    let participant = {
        fullName: "John Doe",
        student_id: "2023101234",
        year_and_block: "3-A",
        department: "Computer Science",
    };

    // Fetch data for the event and registered students
    const fetchEventData = async () => {
    try {
        // Fetch event details
        const eventRes = await fetch(`http://localhost:5000/events/${eventId}`);
        if (!eventRes.ok) throw new Error('Failed to fetch event details');
        event = await eventRes.json();

        // Fetch registered students
        const registrationRes = await fetch(`http://localhost:5000/api/event_registration/${eventId}`);
        if (!registrationRes.ok) throw new Error('Failed to fetch registered students');
        const registrationData = await registrationRes.json();
        registeredStudents = registrationData.registrations; // Access the `registrations` array

         // Fetch attendance records
        const attendanceRes = await fetch(`http://localhost:5000/api/event_attendance/${eventId}`);
        if (!attendanceRes.ok) throw new Error('Failed to fetch attendance records');
        const attendanceData = await attendanceRes.json();
        attendanceRecords = attendanceData.attendance; // Access the `attendance` array

        loading = false;
    } catch (err: any) {
        error = err.message;
        loading = false;
    }
};


    // Watch for changes in page and extract eventId from URL
    $: page.subscribe((p) => {
        const id = p.url.searchParams.get('id'); // Extract `id` from query params
        eventId = parseInt(id ?? '0', 10); // Use '0' as fallback if `id` is null
        console.log('Extracted eventId:', eventId);
    });

    // Trigger data fetching if eventId is valid
    $: if (eventId && !isNaN(eventId) && eventId > 0) {
        fetchEventData();
    } else {
        error = 'Invalid or missing eventId';
        loading = false;
    }

    // Back to events main page
    const goBack = () => {
        goto('/Eventmain');
    };

    // Function to start the QR scanning process
const openModal = async () => {
    showModal = true;
    try {
        videoStream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: "environment" },
        });
        const videoElement = document.querySelector<HTMLVideoElement>("#cameraPreview");
        if (videoElement) {
            videoElement.srcObject = videoStream;
            await videoElement.play();
            startQRScanning(videoElement);
        } else {
            console.error("Video element not found");
        }
    } catch (error) {
        console.error("Error accessing camera:", error);
    }
};

        // Function to close the modal
        const closeModal = () => {
            showModal = false;
            if (videoStream) {
                const tracks = videoStream.getTracks();
                tracks.forEach((track) => track.stop());
                videoStream = null; // Clean up the reference
            }
        };

        // Function to start QR code scanning
        const startQRScanning = (videoElement: HTMLVideoElement) => {
            const canvas = document.createElement("canvas");
            const context = canvas.getContext("2d");

            const scan = () => {
                if (!showModal || !context) return;

                canvas.width = videoElement.videoWidth;
                canvas.height = videoElement.videoHeight;
                context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

                const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
                const code = jsQR(imageData.data, canvas.width, canvas.height);

                if (code) {
                    alert(`QR Code Detected: ${code.data}`);
                    closeModal(); // Close modal after detecting a QR code
                } else {
                    requestAnimationFrame(scan);
                }
            };

            scan();
        };
</script>



<style>
    .modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.6);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }

    .modal-content {
        background: white;
        width: 80%;
        height: 70%;
        display: flex;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }

    .left-section,
    .right-section {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }

    .left-section {
        background-color: #f7f7f7;
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
    }

    .right-section video {
        width: 100%;
        height: auto;
        border-radius: 8px;
    }

    .close-button {
        position: absolute;
        top: 16px;
        right: 16px;
        background: #ff4d4d;
        color: white;
        border: none;
        padding: 8px 12px;
        border-radius: 6px;
        cursor: pointer;
        transition: background-color 0.2s;
    }

    .close-button:hover {
        background-color: #e60000;
    }
    </style>

{#if loading}
    <div>Loading...</div>
{:else}
    {#if error}
        <div class="text-red-500">Error: {error}</div>
    {:else}
        {#if event && registeredStudents}
            <div>
                <!-- Event Header -->
                <div class="flex items-start justify-between p-3 mb-4 bg-gradient-to-r from-[#400000] to-white">
                    <!-- Back Button -->
                    <button 
                        on:click={goBack} 
                        aria-label="Back to Events"
                        class="mr-4 mt-3 text-orange-400 hover:text-gray-800 transition">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                        </svg>
                    </button>

                    <!-- Event Details -->
                    <div class="flex-1">
                        <h1 class="text-2xl font-bold text-white">{event.event_name}</h1>
                        <p class="text-sm text-white mt-1">{event.description}</p>
                    </div>

                    <!-- Modal Trigger Button -->
                    <button
                        on:click={openModal}
                        class="bg-orange-500 text-white px-6 py-2 rounded-lg shadow-lg hover:bg-orange-600 hover:shadow-xl transition duration-200">
                        Start QR Scanning
                    </button>
                </div>

                <!-- Modal -->
                {#if showModal}
                    <div class="modal">
                        <div class="modal-content">
                            <!-- Left Section -->
                            <div class="left-section">
                                <p class="text-gray-700">Event ID: {eventId}</p>
                                <p class="text-gray-700">Event Name: {event.event_name}</p>
                                <p class="text-gray-700">Location: {event.location}</p>
                                <p class="text-gray-700">Name: {participant.fullName}</p>
                                <p class="text-gray-700">Student ID: {participant.student_id}</p>
                                <p class="text-gray-700">Year and Block: {participant.year_and_block}</p>
                                <p class="text-gray-700">Department: {participant.department}</p>
                            </div>

                            <!-- Right Section -->
                            <div class="right-section">
                                <video id="cameraPreview" autoplay playsinline></video>
                            </div>
                        </div>

                        <!-- Close Button -->
                        <button class="close-button" on:click={closeModal}>Close</button>
                    </div>
                {/if}

                <!-- Event Info -->
                <div class="grid grid-cols-5 gap-2 mb-6 p-3">
                    <div class="flex flex-col">
                        <span class="font-medium mb-1">Location</span>
                        <span class="text-gray-600">{event.location}</span>
                    </div>
                    <div class="flex flex-col">
                        <span class="font-medium mb-1">Date</span>
                        <span class="text-gray-600">{event.event_date}</span>
                    </div>
                    <div class="flex flex-col">
                        <span class="font-medium mb-1">Start Time</span>
                        <span class="text-gray-600">{event.start_time}</span>
                    </div>
                    <div class="flex flex-col">
                        <span class="font-medium mb-1">End Time</span>
                        <span class="text-gray-600">{event.end_time}</span>
                    </div>
                    <div class="flex flex-col">
                        <span class="font-medium mb-1">Speaker</span>
                        <span class="text-gray-600">{event.speaker}</span>
                    </div>
                </div>

                <!-- Parent Container with Flexbox -->
                <div class="flex gap-4 p-3">
                    <!-- Attendance Info -->
                    <div class="bg-gray-100 p-3 rounded-md w-1/2">
                        <div class="flex items-center justify-between">
                            <h2 class="text-lg font-semibold text-gray-800">Attendance of Students</h2>
                            <p class="text-2xl font-bold text-orange-400">{attendanceRecords.length}</p>
                        </div>

                        <div class="overflow-x-auto mt-4">
                            <table class="table-auto w-full border-collapse border border-gray-300 text-left">
                                <thead>
                                    <tr class="bg-gray-200 text-gray-800">
                                        <th class="border border-gray-300 px-2 py-2">Student ID</th>
                                        <th class="border border-gray-300 px-2 py-2">FirstName</th>
                                        <th class="border border-gray-300 px-2 py-2">LastName</th>
                                        <th class="border border-gray-300 px-2 py-2">Year and Block</th>
                                        <th class="border border-gray-300 px-2 py-2">Department</th>
                                        <th class="border border-gray-300 px-2 py-2">Check-in</th>
                                        <th class="border border-gray-300 px-2 py-2">Check-out</th>
                                        <th class="border border-gray-300 px-2 py-2">Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {#if attendanceRecords.length > 0}
                                        {#each attendanceRecords as record}
                                            <tr class="hover:bg-gray-100">
                                                <td class="border border-gray-300 px-4 py-2">{record.student_id}</td>
                                                <td class="border border-gray-300 px-4 py-2">{record.firstName}</td>
                                                <td class="border border-gray-300 px-4 py-2">{record.lastName}</td>
                                                <td class="border border-gray-300 px-4 py-2">{record.year_and_block}</td>
                                                <td class="border border-gray-300 px-4 py-2">{record.department}</td>
                                                <td class="border border-gray-300 px-4 py-2">{record.check_in || 'N/A'}</td>
                                                <td class="border border-gray-300 px-4 py-2">{record.check_out || 'N/A'}</td>
                                                <td class="border border-gray-300 px-4 py-2">{record.status}</td>
                                            </tr>
                                        {/each}
                                    {:else}
                                        <tr>
                                            <td colspan="7" class="border border-gray-300 px-4 py-2 text-center text-gray-500">
                                                No attendance records found.
                                            </td>
                                        </tr>
                                    {/if}
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Registered Students Table -->
                    <div class="bg-gray-100 p-3 rounded-md w-1/2">
                        <div class="flex items-center justify-between">
                            <h2 class="text-lg font-semibold text-gray-800">Registered Students</h2>
                            <p class="text-2xl font-bold text-orange-400">{registeredStudents.length}</p>
                        </div>

                        <div class="overflow-x-auto mt-4">
                            <table class="table-auto w-full border-collapse border border-gray-300 text-left">
                                <thead>
                                    <tr class="bg-gray-200 text-gray-800">
                                        <th class="border border-gray-300 px-3 py-2">Student ID</th>
                                        <th class="border border-gray-300 px-3 py-2">FirstName</th>
                                        <th class="border border-gray-300 px-3 py-2">LastName</th>
                                        <th class="border border-gray-300 px-3 py-2">Year and Block</th>
                                        <th class="border border-gray-300 px-3 py-2">Department</th>
                                        <th class="border border-gray-300 px-3 py-2">Registration Date</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {#if registeredStudents.length > 0}
                                        {#each registeredStudents as student}
                                            <tr class="hover:bg-gray-100">
                                                <td class="border border-gray-300 px-4 py-2">{student.student_id}</td>
                                                <td class="border border-gray-300 px-4 py-2">{student.firstName}</td>
                                                <td class="border border-gray-300 px-4 py-2">{student.lastName}</td>
                                                <td class="border border-gray-300 px-4 py-2">{student.year_and_block}</td>
                                                <td class="border border-gray-300 px-4 py-2">{student.department}</td>
                                                <td class="border border-gray-300 px-4 py-2">{student.registration_date || 'N/A'}</td>
                                            </tr>
                                    {/each}
                                    {:else}
                                        <tr>
                                            <td colspan="5" class="border border-gray-300 px-4 py-2 text-center text-gray-500">
                                                No registered students found.
                                            </td>
                                        </tr>
                                    {/if}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        {/if}
    {/if}
{/if}



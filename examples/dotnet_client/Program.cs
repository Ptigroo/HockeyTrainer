using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text.Json;
using System.Threading.Tasks;

namespace HockeyTrainerClient
{
    class Program
    {
        private const string ApiBaseUrl = "http://localhost:8000";

        static async Task Main(string[] args)
        {
            Console.WriteLine("Hockey Trainer - Video Upload Client");
            Console.WriteLine("=====================================\n");

            // Get video file path from user or command line
            string videoPath = GetVideoPath(args);
            
            if (string.IsNullOrEmpty(videoPath) || !File.Exists(videoPath))
            {
                Console.WriteLine("Error: Video file not found.");
                Console.WriteLine("Usage: dotnet run [path/to/video.mp4]");
                return;
            }

            Console.WriteLine($"Video file: {videoPath}");
            Console.WriteLine($"API endpoint: {ApiBaseUrl}/infer/video\n");

            // Upload video and get results
            await UploadVideoAsync(videoPath);

            Console.WriteLine("\nPress any key to exit...");
            Console.ReadKey();
        }

        static string GetVideoPath(string[] args)
        {
            // Check command line arguments first
            if (args.Length > 0 && !string.IsNullOrEmpty(args[0]))
            {
                return args[0];
            }

            // Prompt user for path
            Console.Write("Enter video file path (or drag and drop file here): ");
            string input = Console.ReadLine()?.Trim();
            
            // Remove quotes if present (from drag and drop)
            if (!string.IsNullOrEmpty(input))
            {
                input = input.Trim('"', '\'');
            }

            return input ?? string.Empty;
        }

        static async Task UploadVideoAsync(string videoPath)
        {
            try
            {
                Console.WriteLine("Connecting to API...");

                using var httpClient = new HttpClient();
                httpClient.Timeout = TimeSpan.FromMinutes(5); // Allow time for large videos

                // Check API health first
                var healthResponse = await httpClient.GetAsync($"{ApiBaseUrl}/health");
                if (!healthResponse.IsSuccessStatusCode)
                {
                    Console.WriteLine("Warning: API health check failed. Proceeding anyway...");
                }
                else
                {
                    Console.WriteLine("✓ API is healthy\n");
                }

                // Prepare multipart form data
                using var form = new MultipartFormDataContent();
                using var fileStream = File.OpenRead(videoPath);
                using var streamContent = new StreamContent(fileStream);
                
                // Set content type
                streamContent.Headers.ContentType = new MediaTypeHeaderValue("video/mp4");
                
                // Add file to form
                form.Add(streamContent, "file", Path.GetFileName(videoPath));

                Console.WriteLine("Uploading video...");
                var fileInfo = new FileInfo(videoPath);
                Console.WriteLine($"File size: {fileInfo.Length / 1024.0 / 1024.0:F2} MB");

                // Upload video
                var response = await httpClient.PostAsync($"{ApiBaseUrl}/infer/video", form);

                if (response.IsSuccessStatusCode)
                {
                    Console.WriteLine("✓ Upload successful\n");
                    
                    // Parse and display results
                    var jsonResponse = await response.Content.ReadAsStringAsync();
                    DisplayResults(jsonResponse);
                }
                else
                {
                    Console.WriteLine($"✗ Upload failed: {response.StatusCode}");
                    var errorContent = await response.Content.ReadAsStringAsync();
                    Console.WriteLine($"Error details: {errorContent}");
                }
            }
            catch (HttpRequestException ex)
            {
                Console.WriteLine($"✗ Connection error: {ex.Message}");
                Console.WriteLine("\nMake sure the API service is running:");
                Console.WriteLine("  cd services/api");
                Console.WriteLine("  python main.py");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"✗ Error: {ex.Message}");
            }
        }

        static void DisplayResults(string jsonResponse)
        {
            try
            {
                Console.WriteLine("Analysis Results:");
                Console.WriteLine("=================\n");

                // Pretty print JSON
                using var doc = JsonDocument.Parse(jsonResponse);
                var options = new JsonSerializerOptions { WriteIndented = true };
                var formatted = JsonSerializer.Serialize(doc, options);
                Console.WriteLine(formatted);

                // Extract key metrics if available
                var root = doc.RootElement;
                
                if (root.TryGetProperty("analysis", out var analysis))
                {
                    Console.WriteLine("\n--- Key Metrics ---");
                    
                    if (analysis.TryGetProperty("ball_tracking", out var ballTracking))
                    {
                        if (ballTracking.TryGetProperty("max_speed_kmh", out var maxSpeed))
                        {
                            Console.WriteLine($"Max Ball Speed: {maxSpeed.GetDouble():F1} km/h");
                        }
                        if (ballTracking.TryGetProperty("detections_count", out var count))
                        {
                            Console.WriteLine($"Ball Detections: {count.GetInt32()}");
                        }
                    }

                    if (analysis.TryGetProperty("action_recognition", out var actionRecog))
                    {
                        if (actionRecog.TryGetProperty("actions_detected", out var actions))
                        {
                            Console.WriteLine($"Actions Detected: {actions.GetArrayLength()}");
                        }
                    }
                }

                if (root.TryGetProperty("note", out var note))
                {
                    Console.WriteLine($"\nNote: {note.GetString()}");
                }
            }
            catch (JsonException ex)
            {
                Console.WriteLine($"Error parsing results: {ex.Message}");
                Console.WriteLine($"Raw response: {jsonResponse}");
            }
        }
    }
}

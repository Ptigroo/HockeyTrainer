using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using System.Text.Json;

class Program
{
    static async Task Main(string[] args)
    {
        if (args.Length < 2)
        {
            Console.WriteLine("Usage: dotnet run -- <serverUrl> <videoFilePath>");
            return;
        }

        string serverUrl = args[0].TrimEnd('/');
        string videoPath = args[1];

        if (!File.Exists(videoPath))
        {
            Console.WriteLine($"File not found: {videoPath}");
            return;
        }

        using var http = new HttpClient();
        using var form = new MultipartFormDataContent();
        using var fs = File.OpenRead(videoPath);
        var streamContent = new StreamContent(fs);
        streamContent.Headers.ContentType = new MediaTypeHeaderValue("video/mp4");
        form.Add(streamContent, "file", Path.GetFileName(videoPath));

        Console.WriteLine($"Uploading {videoPath} to {serverUrl}/infer/video ...");
        var resp = await http.PostAsync($"{serverUrl}/infer/video", form);
        resp.EnsureSuccessStatusCode();

        var body = await resp.Content.ReadAsStringAsync();
        using var doc = JsonDocument.Parse(body);
        Console.WriteLine("Response JSON:");
        Console.WriteLine(JsonSerializer.Serialize(doc.RootElement, new JsonSerializerOptions { WriteIndented = true }));
    }
}

using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;
using System.Text.Json;

namespace ChatbotApp.Controllers
{
    [ApiController]
    [Route("api/chatbot")]
    public class ChatbotController : ControllerBase
    {

        [HttpPost]
        public IActionResult Post([FromBody] JsonElement data)
        {
            var userQuery = data.GetProperty("message").GetString();

            var response = Respond(userQuery);

            Console.WriteLine(response);

            return Ok(new { message = "Successful", result = response });
        }

        private static string Respond(string userQuery)
        {
            var start = new ProcessStartInfo
            {
                FileName = "python",
                Arguments = $"chatbot_script.py \"{userQuery}\"",
                UseShellExecute = false,
                RedirectStandardOutput = true,
                CreateNoWindow = true
            };

            using (var process = Process.Start(start))
            {
                using (var reader = process.StandardOutput)
                {
                    var result = reader.ReadToEnd();
                    return result.Trim();
                }
            }
        }
    }
}

const fetch = require('node-fetch');

module.exports = async (req, res) => {
    try {
        // Extract channel ID from the URL
        const { channel } = req.query;
        if (!channel) {
            return res.status(400).send("No channel specified. Use /api/stream?channel=yourChannelID");
        }

        // Construct the play URL with the stream ID
        const playUrl = `https://secureplayer.sportstvn.com/token.php?stream=${channel}`;

        // Fetch the token
        const response = await fetch(playUrl, {
            headers: { Referer: "https://sportstvn.com/" },
        });

        const text = await response.text();

        // Extract token using regex
        const match = text.match(/token=([a-f0-9\-]+)/);
        if (!match) {
            return res.status(500).send("Token not found in the response.");
        }

        const token = match[1];
        const m3u8Url = `https://cdn.sturls.com/${channel}/index.m3u8?token=${encodeURIComponent(token)}`;

        // Redirect to the M3U8 URL
        res.redirect(m3u8Url);

    } catch (error) {
        res.status(500).send("Error fetching stream.");
    }
};

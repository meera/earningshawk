"""
Speaker Photo Search Utility

Searches for speaker headshots on the web and downloads them for use in:
- Video compositions (Remotion SpeakerLabel component)
- Thumbnail generation (speaker overlays)

Usage:
    python speaker_search.py --insights-path /var/earninglens/HOOD/Q3-2025/insights.json
"""

import os
import sys
import json
import logging
import requests
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import quote_plus

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SpeakerPhotoSearch:
    """Search and download speaker headshots from the web"""

    def __init__(self, output_dir: str = "/var/earninglens/_speaker_photos"):
        """
        Initialize speaker photo search

        Args:
            output_dir: Directory to store downloaded speaker photos
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Google Custom Search API (optional - set in .env)
        self.google_api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
        self.google_cx = os.getenv("GOOGLE_SEARCH_CX")

    def search_speaker_photo(
        self,
        name: str,
        role: Optional[str] = None,
        company: Optional[str] = None
    ) -> Optional[str]:
        """
        Search for speaker headshot photo

        Args:
            name: Full name of the speaker (e.g., "Vlad Tenev")
            role: Job title (e.g., "CEO")
            company: Company name (e.g., "Robinhood")

        Returns:
            URL of the best headshot photo, or None if not found
        """
        logger.info(f"Searching for photo: {name} ({role} at {company})")

        # Try multiple search strategies
        strategies = [
            self._search_google_images,
            self._search_linkedin,
            self._search_company_website,
        ]

        for strategy in strategies:
            try:
                photo_url = strategy(name, role, company)
                if photo_url:
                    logger.info(f"Found photo via {strategy.__name__}: {photo_url}")
                    return photo_url
            except Exception as e:
                logger.warning(f"Strategy {strategy.__name__} failed: {e}")
                continue

        logger.warning(f"No photo found for {name}")
        return None

    def _search_google_images(
        self,
        name: str,
        role: Optional[str] = None,
        company: Optional[str] = None
    ) -> Optional[str]:
        """
        Search Google Images using Custom Search API

        Requires GOOGLE_SEARCH_API_KEY and GOOGLE_SEARCH_CX environment variables
        """
        if not self.google_api_key or not self.google_cx:
            logger.debug("Google Custom Search API not configured, skipping")
            return None

        # Build search query
        query_parts = [name]
        if company:
            query_parts.append(company)
        if role:
            query_parts.append(role)
        query_parts.append("headshot")

        query = " ".join(query_parts)

        # Call Google Custom Search API
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.google_api_key,
            "cx": self.google_cx,
            "q": query,
            "searchType": "image",
            "imgSize": "medium",  # Medium size headshots
            "imgType": "face",    # Focus on faces
            "num": 5,             # Get top 5 results
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Return first result
        if "items" in data and len(data["items"]) > 0:
            return data["items"][0]["link"]

        return None

    def _search_linkedin(
        self,
        name: str,
        role: Optional[str] = None,
        company: Optional[str] = None
    ) -> Optional[str]:
        """
        Construct likely LinkedIn profile URL

        Note: This doesn't actually scrape LinkedIn (against TOS).
        Instead, it returns a placeholder URL that can be manually replaced.

        For production, you'd want to:
        1. Use LinkedIn API (requires partnership)
        2. Use a third-party service (Clearbit, Hunter.io, etc.)
        3. Manually curate speaker photos in database
        """
        # Normalize name for LinkedIn URL
        name_slug = name.lower().replace(" ", "-")

        # Return placeholder (for MVP, use default avatar)
        # In production, integrate with Clearbit or similar service
        logger.debug(f"LinkedIn strategy not implemented (use Clearbit API)")
        return None

    def _search_company_website(
        self,
        name: str,
        role: Optional[str] = None,
        company: Optional[str] = None
    ) -> Optional[str]:
        """
        Search company's leadership page for speaker photo

        Many companies have /about/leadership or /team pages with headshots.
        This is a placeholder for MVP.
        """
        logger.debug(f"Company website search not implemented")
        return None

    def download_photo(self, photo_url: str, speaker_name: str) -> str:
        """
        Download speaker photo to local storage

        Args:
            photo_url: URL of the photo to download
            speaker_name: Name of the speaker (for filename)

        Returns:
            Local file path to downloaded photo
        """
        # Generate consistent filename
        name_hash = hashlib.md5(speaker_name.encode()).hexdigest()[:8]
        safe_name = speaker_name.lower().replace(" ", "_")
        filename = f"{safe_name}_{name_hash}.jpg"
        output_path = self.output_dir / filename

        # Download if not already cached
        if output_path.exists():
            logger.info(f"Using cached photo: {output_path}")
            return str(output_path)

        logger.info(f"Downloading photo from {photo_url}")

        try:
            response = requests.get(photo_url, timeout=10, stream=True)
            response.raise_for_status()

            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            logger.info(f"Photo saved to {output_path}")
            return str(output_path)

        except Exception as e:
            logger.error(f"Failed to download photo: {e}")
            raise

    def enrich_insights_with_photos(self, insights_path: str) -> Dict:
        """
        Load insights.json, search for speaker photos, and add photo URLs

        Args:
            insights_path: Path to insights.json file

        Returns:
            Updated insights dictionary with photo URLs
        """
        logger.info(f"Enriching insights with speaker photos: {insights_path}")

        # Load insights
        with open(insights_path, 'r') as f:
            insights = json.load(f)

        # Process each person entity
        if "entities" in insights and "people" in insights["entities"]:
            for person in insights["entities"]["people"]:
                name = person.get("name")
                role = person.get("role")
                company = person.get("company")

                if not name:
                    continue

                # Initialize photo fields if they don't exist
                if "photoUrl" not in person:
                    person["photoUrl"] = None
                if "photoLocalPath" not in person:
                    person["photoLocalPath"] = None

                # Skip if photo already exists
                if person.get("photoUrl"):
                    logger.info(f"⊙ Photo already exists for {name}")
                    continue

                # Search for photo
                photo_url = self.search_speaker_photo(name, role, company)

                if photo_url:
                    # Download photo
                    try:
                        local_path = self.download_photo(photo_url, name)
                        person["photoUrl"] = photo_url
                        person["photoLocalPath"] = local_path
                        logger.info(f"✓ Added photo for {name}")
                    except Exception as e:
                        logger.error(f"✗ Failed to download photo for {name}: {e}")
                        person["photoUrl"] = None
                        person["photoLocalPath"] = None
                else:
                    logger.warning(f"✗ No photo found for {name}")
                    person["photoUrl"] = None
                    person["photoLocalPath"] = None

        # Save updated insights
        output_path = insights_path.replace(".json", ".with_photos.json")
        with open(output_path, 'w') as f:
            json.dump(insights, f, indent=2)

        logger.info(f"Updated insights saved to {output_path}")

        # Also update original file
        with open(insights_path, 'w') as f:
            json.dump(insights, f, indent=2)

        return insights


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Search for speaker headshot photos")
    parser.add_argument(
        "--insights-path",
        required=True,
        help="Path to insights.json file"
    )
    parser.add_argument(
        "--output-dir",
        default="/var/earninglens/_speaker_photos",
        help="Directory to store downloaded photos"
    )

    args = parser.parse_args()

    # Initialize searcher
    searcher = SpeakerPhotoSearch(output_dir=args.output_dir)

    # Enrich insights with photos
    insights = searcher.enrich_insights_with_photos(args.insights_path)

    # Print summary
    people_count = len(insights.get("entities", {}).get("people", []))
    photos_found = sum(
        1 for p in insights.get("entities", {}).get("people", [])
        if p.get("photoUrl")
    )

    print(f"\n✓ Speaker Photo Search Complete")
    print(f"  People found: {people_count}")
    print(f"  Photos found: {photos_found}")
    print(f"  Success rate: {photos_found}/{people_count}")


if __name__ == "__main__":
    main()

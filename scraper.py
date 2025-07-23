import asyncio
from playwright.async_api import async_playwright

async def scrape_skybox():
    """Scrapes Skybox Cinemas website for movie titles."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://skyboxcinemas.com.bo/")
        movies = await page.locator('.movie-title').all_text_contents()
        await browser.close()
        return movies

async def scrape_prime():
    """Scrapes Prime Cinemas website for movie titles."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://primecinemas.com.bo/")
        movies = await page.locator('.movie-info h3').all_text_contents()
        await browser.close()
        return movies

async def scrape_cinemas():
    """Scrapes both Skybox and Prime Cinemas websites."""
    skybox_movies, prime_movies = await asyncio.gather(
        scrape_skybox(),
        scrape_prime()
    )
    return {
        "skybox": skybox_movies,
        "prime": prime_movies
    }

if __name__ == "__main__":
    async def main():
        movies = await scrape_cinemas()
        print(movies)

    asyncio.run(main())

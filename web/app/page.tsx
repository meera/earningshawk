import { Suspense } from 'react';
import Link from 'next/link';
import { Logo } from '@/components/Logo';
import { UserProfileMenu } from '@/components/UserProfileMenu';
import { getCompanies, getSectors, getTopCompaniesByMarketCap } from '@/lib/db/companies';
import { SearchForm } from '@/components/SearchForm';
import { SectorLink } from '@/components/SectorLink';

export const metadata = {
  title: 'Markey HawkEye - Stock Earnings Call Videos',
  description: 'Browse earnings call videos for 7,600+ public companies. Listen to actual executive voices with synchronized financial data.',
  openGraph: {
    title: 'Markey HawkEye - Stock Earnings Call Videos',
    description: 'Browse earnings call videos for 7,600+ public companies.',
  },
};

function formatMarketCap(marketCap: number | null): string {
  if (!marketCap) return 'N/A';

  const billion = 1_000_000_000;
  const million = 1_000_000;

  if (marketCap >= billion) {
    return `$${(marketCap / billion).toFixed(1)}B`;
  } else if (marketCap >= million) {
    return `$${(marketCap / million).toFixed(0)}M`;
  } else {
    return `$${marketCap.toLocaleString()}`;
  }
}

async function TopCompanies() {
  const topCompanies = await getTopCompaniesByMarketCap(20);

  return (
    <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
      {topCompanies.map((company) => (
        <Link
          key={company.id}
          href={`/companies/${company.slug}`}
          className="group bg-background-muted/40 border border-border rounded-xl p-4 hover:bg-background-muted/60 hover:border-border-accent hover:shadow-lg hover:shadow-accent/10 transition-all"
        >
          <div className="flex items-start justify-between mb-2">
            <div>
              <div className="text-primary font-bold text-lg group-hover:text-primary-light transition-colors">
                {company.ticker}
              </div>
              <div className="text-text-tertiary text-xs mt-1">{company.metadata.sector || 'N/A'}</div>
            </div>
            <div className="text-xs text-text-tertiary bg-background/50 px-2 py-1 rounded">
              {formatMarketCap(company.metadata.market_cap || null)}
            </div>
          </div>
          <div className="text-text-secondary text-sm line-clamp-2">{company.name}</div>
        </Link>
      ))}
    </div>
  );
}

async function SectorsList() {
  const sectors = await getSectors();

  return (
    <div className="flex flex-wrap gap-2">
      {sectors.map((sector) => (
        <SectorLink key={sector.sector} sector={sector.sector} count={sector.count} />
      ))}
    </div>
  );
}

export default async function HomePage({
  searchParams,
}: {
  searchParams: Promise<{ sector?: string; search?: string }>;
}) {
  const { sector, search } = await searchParams;
  const companies = await getCompanies({
    sector,
    search,
    limit: 100,
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background-elevated to-background">
      {/* Header */}
      <header className="border-b border-border backdrop-blur-sm bg-background/80 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <Logo />

            <nav className="flex items-center space-x-6">
              <Link href="/" className="text-primary font-medium transition-colors text-sm">
                Companies
              </Link>
              <Link href="/pricing" className="text-text-tertiary hover:text-primary transition-colors text-sm">
                Pricing
              </Link>
              <Link href="/about" className="text-text-tertiary hover:text-primary transition-colors text-sm">
                About
              </Link>
              <UserProfileMenu />
            </nav>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Page Title */}
        <div className="mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-text-primary mb-4">
            {search ? `Search Results for "${search}"` : sector ? `${sector} Companies` : 'All Companies'}
          </h1>
          <p className="text-xl text-text-secondary">
            {search
              ? `Found ${companies.length.toLocaleString()} ${companies.length === 1 ? 'company' : 'companies'}`
              : `Browse earnings call videos for 7,600+ public companies`
            }
          </p>
        </div>

        {/* Search Bar - Prominent */}
        <section className="mb-12">
          <SearchForm defaultValue={search} />
          {(search || sector) && (
            <div className="max-w-3xl mx-auto mt-3 text-center">
              <Link
                href="/"
                className="inline-block px-6 py-2 bg-background-muted hover:bg-background-elevated border border-border text-text-secondary hover:text-primary rounded-lg font-semibold transition-all"
              >
                Clear
              </Link>
            </div>
          )}
        </section>

        {/* Top Companies */}
        {!sector && !search && (
          <section className="mb-12">
            <h2 className="text-2xl font-bold text-text-primary mb-6">Top Companies by Market Cap</h2>
            <Suspense fallback={<div className="text-text-tertiary">Loading...</div>}>
              <TopCompanies />
            </Suspense>
          </section>
        )}

        {/* Sectors Filter */}
        {!sector && !search && (
          <section className="mb-12">
            <h2 className="text-2xl font-bold text-text-primary mb-6">Browse by Sector</h2>
            <Suspense fallback={<div className="text-text-tertiary">Loading...</div>}>
              <SectorsList />
            </Suspense>
          </section>
        )}

        {/* Companies List */}
        <section>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {companies.map((company) => (
              <Link
                key={company.id}
                href={`/companies/${company.slug}`}
                className="group bg-background-muted/40 border border-border rounded-xl p-4 hover:bg-background-muted/60 hover:border-border-accent hover:shadow-lg hover:shadow-accent/10 transition-all"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="text-primary font-bold text-lg group-hover:text-primary-light transition-colors">
                    {company.ticker}
                  </div>
                  {company.metadata.market_cap && (
                    <div className="text-xs text-text-tertiary bg-background/50 px-2 py-1 rounded">
                      {formatMarketCap(company.metadata.market_cap)}
                    </div>
                  )}
                </div>
                <div className="text-text-secondary text-sm mb-2 line-clamp-2">{company.name}</div>
                <div className="flex items-center gap-2 text-xs text-text-tertiary">
                  {company.metadata.sector && <span>{company.metadata.sector}</span>}
                  {company.metadata.country && <span>• {company.metadata.country}</span>}
                </div>
              </Link>
            ))}
          </div>

          {companies.length === 0 && (
            <div className="text-center py-12">
              <p className="text-text-tertiary text-lg">No companies found.</p>
            </div>
          )}
        </section>
      </div>

      {/* Footer */}
      <footer className="border-t border-border mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Social Media Section */}
          <div className="text-center mb-8">
            <p className="text-text-secondary text-sm mb-4">Follow us for market insights, earnings analysis & exclusive content</p>
            <div className="flex items-center justify-center gap-6">
              <Link
                href="https://youtube.com/@MarketHawkEyes"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-text-tertiary hover:text-red-500 transition-colors group"
              >
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                </svg>
                <span className="text-sm font-medium group-hover:underline">@MarketHawkEyes</span>
              </Link>

              <Link
                href="https://x.com/MarketHawkEye"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-text-tertiary hover:text-blue-400 transition-colors group"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                </svg>
                <span className="text-sm font-medium group-hover:underline">@MarketHawkEye</span>
              </Link>

              <Link
                href="https://instagram.com/markethawkeye"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-text-tertiary hover:text-pink-500 transition-colors group"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                </svg>
                <span className="text-sm font-medium group-hover:underline">@markethawkeye</span>
              </Link>

              <Link
                href="https://www.reddit.com/user/markethawkeye/"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-text-tertiary hover:text-orange-500 transition-colors group"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0zm5.01 4.744c.688 0 1.25.561 1.25 1.249a1.25 1.25 0 0 1-2.498.056l-2.597-.547-.8 3.747c1.824.07 3.48.632 4.674 1.488.308-.309.73-.491 1.207-.491.968 0 1.754.786 1.754 1.754 0 .716-.435 1.333-1.01 1.614a3.111 3.111 0 0 1 .042.52c0 2.694-3.13 4.87-7.004 4.87-3.874 0-7.004-2.176-7.004-4.87 0-.183.015-.366.043-.534A1.748 1.748 0 0 1 4.028 12c0-.968.786-1.754 1.754-1.754.463 0 .898.196 1.207.49 1.207-.883 2.878-1.43 4.744-1.487l.885-4.182a.342.342 0 0 1 .14-.197.35.35 0 0 1 .238-.042l2.906.617a1.214 1.214 0 0 1 1.108-.701zM9.25 12C8.561 12 8 12.562 8 13.25c0 .687.561 1.248 1.25 1.248.687 0 1.248-.561 1.248-1.249 0-.688-.561-1.249-1.249-1.249zm5.5 0c-.687 0-1.248.561-1.248 1.25 0 .687.561 1.248 1.249 1.248.688 0 1.249-.561 1.249-1.249 0-.687-.562-1.249-1.25-1.249zm-5.466 3.99a.327.327 0 0 0-.231.094.33.33 0 0 0 0 .463c.842.842 2.484.913 2.961.913.477 0 2.105-.056 2.961-.913a.361.361 0 0 0 .029-.463.33.33 0 0 0-.464 0c-.547.533-1.684.73-2.512.73-.828 0-1.979-.196-2.512-.73a.326.326 0 0 0-.232-.095z"/>
                </svg>
                <span className="text-sm font-medium group-hover:underline">u/markethawkeye</span>
              </Link>
            </div>
          </div>

          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0 pt-8 border-t border-border">
            <div className="flex items-center space-x-3">
              <Logo size="small" />
              <span className="text-text-tertiary text-sm">
                © 2024 Markey HawkEye. Transform earnings calls into visual insights.
              </span>
            </div>

            <div className="flex items-center space-x-6 text-sm">
              <Link href="mailto:thehawkeyemarket@gmail.com" className="text-text-tertiary hover:text-accent transition-colors">
                Contact
              </Link>
              <Link href="/about" className="text-text-tertiary hover:text-accent transition-colors">
                About
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

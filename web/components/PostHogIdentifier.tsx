'use client';

import { useEffect } from 'react';
import { useSession } from '@/lib/auth-client';
import posthog from 'posthog-js';

/**
 * Component that identifies users in PostHog when they sign in
 * Handles both email/password and OAuth sign-ins
 * Should be placed in the app layout
 */
export function PostHogIdentifier() {
  const { data: session } = useSession();

  useEffect(() => {
    if (session?.user) {
      const { email, name, id } = session.user;

      // Identify user in PostHog with email as the distinct ID
      if (email) {
        posthog.identify(email, {
          email,
          name: name || undefined,
          user_id: id,
        });

        console.log('[PostHog] User identified:', email);
      }
    } else {
      // Reset identity when logged out
      posthog.reset();
    }
  }, [session]);

  return null; // This component doesn't render anything
}

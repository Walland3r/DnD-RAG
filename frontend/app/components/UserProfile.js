'use client';

import React from 'react';
import { useKeycloak } from '../contexts/KeycloakContext';

const UserProfile = () => {
  const { userInfo, logout } = useKeycloak();

  if (!userInfo) {
    return null;
  }

  return (
    <div className="user-profile">
      <div className="user-info">
        <span className="user-name">
          {userInfo.fullName || userInfo.username}
        </span>
        <button onClick={logout} className="logout-button">
          Sign Out
        </button>
      </div>
    </div>
  );
};

export default UserProfile;

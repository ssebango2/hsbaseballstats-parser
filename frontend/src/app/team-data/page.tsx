'use client';

import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface TeamDataItem {
    [key: string]: string | number;
}

export default function TeamData() {
    const [teamName, setTeamName] = useState<string>('');
    const [teamData, setTeamData] = useState<TeamDataItem[]>([]);
    const [error, setError] = useState<string | null>(null);
    const [availableTeams, setAvailableTeams] = useState<string[]>([]);
    const [loading, setLoading] = useState<boolean>(false);

    useEffect(() => {
        fetchAvailableTeams();
    }, []);

    const fetchAvailableTeams = async () => {
        setLoading(true);
        try {
            const response = await axios.get<{ teams: string[] }>('http://127.0.0.1:5000/api/get_available_teams');
            setAvailableTeams(response.data.teams);
            setError(null);
        } catch (err: any) {
            setError(err.response?.data?.error || 'Error fetching available teams');
            setAvailableTeams([]);
        }
        setLoading(false);
    };

    const handleTeamChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        setTeamName(e.target.value);
    };

    const fetchTeamData = async () => {
        if (!teamName) {
            setError('Please select a team');
            return;
        }

        setLoading(true);
        try {
            const response = await axios.get<{ data: TeamDataItem[] }>(`http://127.0.0.1:5000/api/get_team_data?team_name=${teamName}`);
            setTeamData(response.data.data);
            setError(null);
        } catch (err: any) {
            setError(err.response?.data?.error || 'Error fetching team data');
            setTeamData([]);
        }
        setLoading(false);
    };

    return (
        <div className="p-4">
            <h2 className="text-2xl font-bold mb-4">Baseball Team Data</h2>
            <div className="mb-4">
                <select
                    value={teamName}
                    onChange={handleTeamChange}
                    className="mr-2 p-2 border rounded"
                    disabled={loading || availableTeams.length === 0}
                >
                    <option value="">Select a team</option>
                    {availableTeams.map((team) => (
                        <option key={team} value={team}>
                            {team}
                        </option>
                    ))}
                </select>
                <button
                    onClick={fetchTeamData}
                    className="bg-blue-500 text-white p-2 rounded"
                    disabled={loading || !teamName}
                >
                    {loading ? 'Loading...' : 'Fetch Data'}
                </button>
            </div>

            {error && <p className="text-red-500 mb-4">{error}</p>}

            {teamData.length > 0 && (
                <div className="overflow-x-auto">
                    <table className="min-w-full bg-white border border-gray-300">
                        <thead>
                            <tr className="bg-gray-100">
                                {Object.keys(teamData[0]).map((key) => (
                                    <th key={key} className="p-2 border">
                                        {key}
                                    </th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {teamData.map((row, index) => (
                                <tr key={index} className={index % 2 === 0 ? 'bg-gray-50' : ''}>
                                    {Object.values(row).map((value, i) => (
                                        <td key={i} className="p-2 border">
                                            {value}
                                        </td>
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}
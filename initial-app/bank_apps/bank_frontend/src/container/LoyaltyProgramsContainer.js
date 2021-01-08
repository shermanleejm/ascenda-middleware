import React from 'react';
import LoyaltyProgramComponent from '../component/LoyaltyProgramComponent';

const LoyaltyProgramsContainer = (props) => {

    return (
        <div>
            <h2>{props.loyaltyPrograms.length} Available Loyalty Programs</h2>
            {props.loyaltyPrograms.map(loyaltyProgram => {
                return <LoyaltyProgramComponent user={props.user} loyaltyProgram={loyaltyProgram}/>
            })}
        </div>
    );
}

export default LoyaltyProgramsContainer;

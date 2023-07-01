import React from 'react';

const ActiveCharts = ({moniker, endpoint, amount}) =>
{
    const [mappedElements, setMappedElements] = React.useState([]);
    const [exception, setError] = React.useState(null);

    React.useEffect(() =>
    {
        try
        {
            for (let i=0; i < amount+1; i++) {
                const obj = () =>
                {
                    return <object key={moniker + "-" + i.toString()} data={endpoint + "/" + moniker + i.toString() + ".html"}/>
                };

                setMappedElements((elements) => [...elements, obj()]);
            };
        }
        catch
        {
            setError(exception);
        };
    }, []);

    if (exception)
    {
        return <div>Error: {exception.message}</div>;
    }

    return (
        <div className="populated-components-container">{mappedElements}</div>
    );
}

export default ActiveCharts;